
# Cargo-Guardian

## Overview

`cargo-guardian` is a Python-based utility designed to enhance the security posture of Rust projects by automating the update process of `Cargo.toml` dependencies. Leveraging vulnerability databases, it identifies dependencies within your Rust project that are known to be vulnerable and automatically updates them to versions that have addressed these vulnerabilities.

## Features

- **Automated Vulnerability Patching**: Automatically updates `Cargo.toml` with secure versions of dependencies that have been patched for known vulnerabilities.
- **Custom Update Notifications**: Informs users about the specific dependencies being updated, including the old and new version numbers.
- **Easy Integration**: Designed to be easily integrated into existing Rust project workflows and continuous integration pipelines.
- **Command-Line Interface**: Offers a simple CLI for straightforward execution and integration.

## Requirements

- Python 3.6 or newer
- `toml` Python module
- `pandas` Python module
- `bs4` Python module
- Access to a vulnerability database or CSV file listing vulnerable crate versions and their patched versions.

## Installation

Ensure you have Python installed, then install the required Python packages:

```bash
pip install toml pandas bs4 tqdm
```

Clone the `cargo-guardian` repository:

```bash
git clone https://github.com/muhammad-hassnain/cargo-guardian.git
cd cargo-guardian
```

## Usage

To use `cargo-guardian`, navigate to your Rust project directory and run:

```bash
python path/to/cargo-guardian/protector.py /path/to/your/project
```

To update vulnerability information and check for dependency updates, use the `-U` or `--update` flag:

```bash
python path/to/cargo-guardian/protector.py -U /path/to/your/project
```

## How It Works

1. **Scanning**: `cargo-guardian` scans the `Cargo.toml` file in your Rust project to identify current dependencies.
2. **Checking**: It compares your dependencies against a list of known vulnerabilities.
3. **Updating**: If a vulnerable dependency is found, `cargo-guardian` updates your `Cargo.toml` file with the recommended secure version.

## Contributing

Contributions to `cargo-guardian` are welcome! Whether it's feature requests, bug reports, or code contributions, please feel free to open an issue or a pull request on our GitHub repository.

## License

`cargo-guardian` is licensed under [MIT](LICENSE.md), making it free and open-source software.
