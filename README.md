# A Python Script for Encrypting and Decrypting Files

This script helps you encrypt and decrypt files or directories using strong AES-256-CBC encryption. You can choose between using a password or a key file, making it flexible for different use cases. Dynamic salt ensures that even the same password produces unique encryption results every time.

## Features

- **Key-Based Encryption**:
  - Generate a 256-bit encryption key.
  - Securely store keys in a file for repeated use.

- **Password-Based Encryption**:
  - Use a password to derive an encryption key with PBKDF2.
  - Dynamic salt ensures unique keys even with the same password.

- **File and Directory Support**:
  - Encrypt or decrypt individual files.
  - Recursively encrypt or decrypt all files in a directory.

- **Safety Checks**:
  - Prevent accidental encryption or decryption of critical directories (e.g., root or home).

## Installation

### Prerequisites

- Python 3.7 or higher

### Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd project-folder
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## How to Use the Script

### Generating a Key

To generate a new encryption key and save it to a file:

```bash
python src/encryptf.py --generate-key --key /path/to/keyfile.key
```

If the file already exists, the script will stop and warn you.

### Encrypting a File

To encrypt a single file using a key file:

```bash
python src/encryptf.py --encrypt --file /path/to/file.txt --key /path/to/keyfile.key
```

To encrypt a file using a password:

```bash
python src/encryptf.py --encrypt --file /path/to/file.txt --password "yourpassword"
```

### Decrypting a File

To decrypt a file using a key file:

```bash
python src/encryptf.py --decrypt --file /path/to/file.txt --key /path/to/keyfile.key
```

To decrypt a file using a password:

```bash
python src/encryptf.py --decrypt --file /path/to/file.txt --password "yourpassword"
```

### Encrypting or Decrypting Directories

You can recursively encrypt or decrypt all files in a directory using the `--directory` option:

```bash
python src/encryptf.py --encrypt --directory /path/to/directory --key /path/to/keyfile.key
```

### Security Notes

- **Dynamic Salt**: Each encryption operation generates a random 16-byte salt. This ensures that even with the same password, encryption results are unique.
- **Safety Features**: The script checks for unsafe directories like the home directory or root before proceeding.

## Testing

To run unit tests and verify the script:

```bash
python -m unittest discover -s tests
```

## Project Structure

For those interested in the code:

```bash
project-folder/
├── src/
│   ├── __init__.py       # Makes it a package
│   ├── encryptf.py       # Main script for encryption and decryption
├── tests/
│   ├── test_encrypt_decrypt.py  # Unit tests for the script
├── requirements.txt      # List of dependencies
```

## Contributions

Contributions are welcome! If you have ideas for improvements or new features, feel free to fork the repository, create a feature branch, and submit a pull request.

## License

This script is licensed under the MIT License. See the `LICENSE` file for more details.
