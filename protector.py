import toml
import os
import yaml
import pandas as pd
import re

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
    # return {crate: details.get("version", "Unknown") for crate, details in dependencies.items()}

def dictionary_maker(doc):
    lines = doc.split('\n')
    # print(lines)
    codex = {}
    for line in lines:
        # print(line)
        if line!="":
            temp = line.split(":")
            # print(temp)
            if len(temp) == 2: # no nested
                # print('here' , temp[0] , temp[1])
                codex[temp[0]] = temp[1]
            elif(len(temp) > 2): # nested dict
                outer_key = temp[0]
    
                # Initialize the inner dictionary
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
                # print(temp)
                # vessel = temp[1:]
                # inner_elements_cleaned = vessel.replace("{", "").replace("}", "").split("',")
                # inner_dict = {vessel[i]:vessel[i+1] for i in range(0,len(vessel)-1,2)}
                # print(vessel)
                # print(inner_dict) 
                # codex[temp[0]] = inner_dict
    return codex
    
def searcher(crate, version, contents):
    """
    Search for a crate with the given name and version in the data file.
    """
    # with open(data_file, 'r') as file:
    #     # Split the file into separate documents
    #     documents = file.read().split('---')
    #     # print(documents[0])
    #     for doc in documents:
    #         # print(doc)
    #         if doc.strip():  # Check if the document is not empty
    #             # print(doc)
    #             information = dictionary_maker(doc)
    #             print(information["package"])
    #             # temp = information["package"]
    #             # print(temp["name'"])
    #             # if (crate == information["package"]["name'"]):
    #                 # print("found")
    #             break 
    # return None  # No matching vulnerability found
    # read the csv file as a dataframe
    # print(contents["package_name"])
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
            print('sad')
            return patched_version
    return None


        # print("-----")
        # print( target["unaffected"])
    # print(crate, contents["package_name"])
    # for name in contents["package_name"]:
    #     crate_name = name.split("(")[0]
    #     if(crate == crate_name):
    #         print("in")  
            
def update_cargo_dependencies(cargo_toml_path, new_versions):
    """
    Updates the dependencies in a Cargo.toml file based on a given dictionary.

    :param cargo_toml_path: Path to the Cargo.toml file.
    :param new_versions: Dictionary with dependency names as keys and new versions as values.
    """

    cargo_toml_path = os.path.join(cargo_toml_directory, "Cargo.toml")

    # Read the Cargo.toml file
    with open(cargo_toml_path, 'r') as file:
        cargo_data = toml.load(file)

    # Update the dependencies section if it exists and if the dependency is in new_versions
    if 'dependencies' in cargo_data:
        for dep, new_version in new_versions.items():
            if dep in cargo_data['dependencies']:
                cargo_data['dependencies'][dep] = new_version

    # Write the updated Cargo.toml file back
    with open(cargo_toml_path, 'w') as file:
        toml.dump(cargo_data, file)


# Example usage:
cargo_toml_directory = '/Users/hassnain/Desktop/Research/cargo-guardian/fun'  # Replace with the actual directory containing Cargo.toml
dependencies = get_crate_dependencies(cargo_toml_directory)
# print(dependencies)
# print(searcher())
contents = pd.read_csv('results.csv' , on_bad_lines="skip")
contents['package_name'] = contents['package_name'].str.replace(r'\(crates\.io\)', '', regex=True)
fixes = {}
update = False
for k,v in dependencies.items():
    print(k,v)
    version = searcher(k,v, contents)
    # print(version)
    if version != None:
        fixes[k] = version
        update = True
    else:
        fixes[k] = v
# print(fies)
print(fixes)

if update:
    # requires update
    update_cargo_dependencies(cargo_toml_directory, fixes)