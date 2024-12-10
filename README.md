# EncryptF Project

## Overview

EncryptF is a Python-based tool for securely encrypting and decrypting files and directories. It supports two key management systems: file-based keys and password-based keys, providing flexibility for different use cases. This project uses AES-256-CBC for encryption, ensuring strong security.

## Project Structure

The project is organized as follows:

```bash
project-folder/
├── src/
│   ├── __init__.py       # Makes it a package
│   ├── encryptf.py       # Main script for encryption and decryption
├── tests/
│   ├── test_encrypt_decrypt.py  # Unit tests for EncryptF
├── requirements.txt      # List of dependencies
```

## Features

- **Key-Based Encryption**:
  - Generate a 256-bit encryption key.
  - Load keys from a file for secure operations.

- **Password-Based Encryption**:
  - Derive keys using PBKDF2 and a password for enhanced usability.

- **File and Directory Support**:
  - Encrypt or decrypt individual files.
  - Recursively encrypt or decrypt all files in a directory.

- **Safety Checks**:
  - Prevent accidental encryption or decryption of critical system directories (e.g., root or home).

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

## Usage

### Encrypting and Decrypting

1. Navigate to the `src` directory:

   ```bash
   cd src
   ```

2. **Generate a Key**:

   ```bash
   python encryptf.py --generate-key --key /path/to/keyfile.key
   ```

3. **Encrypt a File**:

   ```bash
   python encryptf.py --encrypt --file /path/to/file.txt --key /path/to/keyfile.key
   ```

4. **Decrypt a File**:

   ```bash
   python encryptf.py --decrypt --file /path/to/file.txt --key /path/to/keyfile.key
   ```

5. **Use a Password**:

   ```bash
   python encryptf.py --encrypt --file /path/to/file.txt --password "yourpassword"
   ```

### Testing

Run unit tests to ensure the tool works as expected:

```bash
python -m unittest discover -s tests
```

## Contributions

Contributions are welcome! Feel free to fork the repository, create a feature branch, and submit a pull request.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
