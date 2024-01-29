import toml
import os
import argparse
import pandas as pd
import re
import getVulnerabilityInfo

def get_crate_dependencies(cargo_toml_directory):
    """
    Reads the Cargo.toml file in the given directory and returns the names and versions of the dependencies.

    :param cargo_toml_directory: Directory containing the Cargo.toml file.
    :return: A dictionary with crate names as keys and their versions as values.
    """
    cargo_toml_path = os.path.join(cargo_toml_directory, "Cargo.toml")
    
    if not os.path.exists(cargo_toml_path):
        raise FileNotFoundError(f"The file {cargo_toml_path} does not exist.")

    with open(cargo_toml_path, 'r') as file:
        cargo_toml = toml.load(file)

    dependencies = cargo_toml.get("dependencies", {})
    # print(type(dependencies))
    return dependencies

def dictionary_maker(doc):
    lines = doc.split('\n')
    codex = {}
    for line in lines:
        if line!="":
            temp = line.split(":")
            if len(temp) == 2: # no nested
                codex[temp[0]] = temp[1]
            elif(len(temp) > 2): # nested dict
                outer_key = temp[0]
                inner_dict = {}
                # Process the list to extract key-value pairs for the inner dictionary
                # The key-value pairs start from index 1 and alternate thereafter
                for i in range(1, len(temp), 2):  # Start from index 1 and skip every other element for keys
                    if i + 1 < len(temp):  # Ensure there's a value for the current key
                        key = temp[i].replace("{'", "").replace(" '", "").strip()  # Clean the key
                        value = temp[i + 1].replace("',", "").replace("'}", "").strip()  # Clean the value
                        inner_dict[key] = value
                
                # Assemble the outer dictionary
                codex[outer_key] = inner_dict
    return codex
    
def searcher(crate, version, contents):
    """
    Search for a crate with the given name and version in the data file.
    """
    target = contents[contents["package_name"] == crate]
    # print(target)
    if target.empty:
        return None
    else:
        # print(target["patched"] 
        patched_version = list(target["patched"])[0]
        # print(patched_version)
        version_pattern = r'\d+\.\d+\.\d+'
        # print(patched_version) = 
        match = re.search(version_pattern , patched_version)
        # print([patched_version])
        patched_version = match.group(0)
        # print(patched_version)
        if version < patched_version:
            # print('sad')
            return patched_version
    return None

def update_cargo_dependencies(cargo_toml_path, new_versions):
    """
    Updates the dependencies in a Cargo.toml file based on a given dictionary,
    and prints a message for each updated dependency.

    :param cargo_toml_path: Path to the Cargo.toml file.
    :param new_versions: Dictionary with dependency names as keys and new versions as values.
    """

    # It seems like there's a redundancy in the provided code snippet. 
    # The `cargo_toml_path` parameter is already expected to be the full path to the Cargo.toml file.
    # Thus, the line below is unnecessary and potentially incorrect since `cargo_toml_directory` is not defined in this scope.
    # cargo_toml_path = os.path.join(cargo_toml_directory, "Cargo.toml")

    cargo_toml_path = os.path.join(cargo_toml_path, "Cargo.toml")
    # Read the Cargo.toml file
    with open(cargo_toml_path, 'r') as file:
        cargo_data = toml.load(file)

    # Update the dependencies section if it exists and if the dependency is in new_versions
    if 'dependencies' in cargo_data:
        for dep, new_version in new_versions.items():
            if dep in cargo_data['dependencies']:
                current_version = cargo_data['dependencies'][dep]
                if current_version != new_version:
                    print(f"{dep} found in rust sec, you are using a vulnerable version {current_version}. Updating the version to {new_version}.")
                    cargo_data['dependencies'][dep] = new_version

    # Write the updated Cargo.toml file back
    with open(cargo_toml_path, 'w') as file:
        toml.dump(cargo_data, file)



if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Update Cargo.toml dependencies based on vulnerability checks.")
    parser.add_argument("-U", "--update", help="Run the getUpdate function to update vulnerability information", action="store_true")
    parser.add_argument("path", help="Path to the directory containing Cargo.toml", type=str)
    
    args = parser.parse_args()
    
    # Use the provided path
    cargo_toml_directory = args.path
    
    # Ensure the path exists
    if not os.path.exists(cargo_toml_directory):
        print(f"The directory {cargo_toml_directory} does not exist.")
        exit()
    
    # Check for the existence of vulnerabilityInfo.csv; if not found, run getUpdate()
    results_csv_path = 'vulnerabilityInfo.csv'
    if not os.path.isfile(results_csv_path) or args.update:
        print("vulnerabilities infroamtion file not found or update requested. Updating vulnerability information...")
        getVulnerabilityInfo.getUpdate()
        
    # Assuming getUpdate() creates or updates vulnerabilityInfo.csv, proceed with reading it
    try:
        contents = pd.read_csv(results_csv_path, on_bad_lines="skip")
        contents['package_name'] = contents['package_name'].str.replace(r'\(crates\.io\)', '', regex=True)
    except FileNotFoundError:
        print("Unable to find or create vulnerabilityInfo.csv. Exiting.")
        exit()
    
    dependencies = get_crate_dependencies(cargo_toml_directory)
    
    fixes = {}
    update_needed = False
    for k, v in dependencies.items():
        version = searcher(k, v, contents)
        if version is not None:
            fixes[k] = version
            update_needed = True
        else:
            fixes[k] = v

    if update_needed:
        update_cargo_dependencies(cargo_toml_directory, fixes)