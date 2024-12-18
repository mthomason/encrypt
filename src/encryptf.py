# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright © Michael Thomason 2024.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import argparse
import tempfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
import base64
import secrets

# Default key file location
DEFAULT_KEY_FILEPATH = os.path.expanduser("~/.encryption_key")
KEY_SIZE = 32  # 256-bit key
IV_SIZE = 16   # AES block size

# Functions shared between operations
def load_key(key_filepath):
	"""Load the encryption key from a file."""
	with open(key_filepath, 'rb') as key_file:
		return base64.b64decode(key_file.read())

def derive_key_from_password(password, salt):
	"""Derive a key from a password using PBKDF2."""
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=KEY_SIZE,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)
	return kdf.derive(password.encode())

def generate_key(key_filepath):
	"""Generate and save a new 256-bit encryption key."""
	if os.path.exists(key_filepath):
		print(f"Error: Key file '{key_filepath}' already exists. Key generation aborted.")
		sys.exit(1)
	key = secrets.token_bytes(KEY_SIZE)
	os.makedirs(os.path.dirname(key_filepath), exist_ok=True)
	with open(key_filepath, 'wb') as key_file:
		key_file.write(base64.b64encode(key))
	print(f"Key has been generated and saved to '{key_filepath}'")

def is_safe_directory(directory_path):
	"""Check if the directory is safe to process."""
	unsafe_paths = [os.path.expanduser("~"), "/", "C:\\"]
	return os.path.abspath(directory_path) not in map(os.path.abspath, unsafe_paths)

# Encryption functions
def encrypt_data(data, key):
	"""Encrypt data using AES-256-CBC."""
	iv = secrets.token_bytes(IV_SIZE)
	salt = secrets.token_bytes(16)  # Generate a 16-byte random salt
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	encryptor = cipher.encryptor()
	padder = PKCS7(algorithms.AES.block_size).padder()
	padded_data = padder.update(data) + padder.finalize()
	encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
	return base64.b64encode(salt + iv + encrypted_data)

def decrypt_data(encrypted_data, key):
	"""Decrypt data using AES-256-CBC."""
	decoded_data = base64.b64decode(encrypted_data)
	salt, iv, encrypted_message = decoded_data[:16], decoded_data[16:16+IV_SIZE], decoded_data[16+IV_SIZE:]
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	decryptor = cipher.decryptor()
	unpadder = PKCS7(algorithms.AES.block_size).unpadder()
	padded_data = decryptor.update(encrypted_message) + decryptor.finalize()
	return unpadder.update(padded_data) + unpadder.finalize()

def encrypt_file(file_path, key):
	"""Encrypt a single file, using a temporary file to avoid overwriting issues."""
	try:
		with open(file_path, 'rb') as file:
			data = file.read()
		encrypted_data = encrypt_data(data, key)
		with tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(file_path)) as temp_file:
			temp_file.write(encrypted_data)
			temp_filename = temp_file.name
		os.replace(temp_filename, file_path)
		print(f"Encrypted: {file_path}")
	except FileNotFoundError as e:
		print(f"File not found: {file_path}: {e}")
	except PermissionError as e:
		print(f"Permission denied while accessing {file_path}: {e}")
	except IOError as e:
		print(f"I/O error occurred while processing {file_path}: {e}")
	except ValueError as e:
		print(f"Encryption failed due to invalid data or key: {e}") 
	except Exception as e:
		print(f"An unexpected error occurred while encrypting {file_path}: {e}") 

def encrypt_directory(directory_path, key):
	"""Encrypt all files in the specified directory."""
	for root, _, files in os.walk(directory_path):
		for file in files:
			file_path = os.path.join(root, file)
			encrypt_file(file_path, key)

# Decryption functions
def decrypt_file(file_path, key):
	"""Decrypt a single file using a temporary file."""
	try:
		with open(file_path, 'rb') as file:
			encrypted_data = file.read()
		decrypted_data = decrypt_data(encrypted_data, key)
		with tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(file_path)) as temp_file:
			temp_file.write(decrypted_data)
			temp_filename = temp_file.name
		os.replace(temp_filename, file_path)
		print(f"Decrypted: {file_path}")
	except FileNotFoundError as e: 
		print(f"File not found: {file_path}: {e}")
	except PermissionError as e:
		print(f"Permission denied: {file_path}: {e}")
	except IOError as e:
		print(f"I/O error occurred while accessing {file_path}: {e}")
	except ValueError as e:
		print(f"Decryption failed due to invalid data or key in {file_path}: {e}")
	except Exception as e:
		print(f"Failed to decrypt {file_path}: {e}")

def decrypt_directory(directory_path, key):
	"""Decrypt all files in the specified directory."""
	for root, _, files in os.walk(directory_path):
		for file in files:
			file_path = os.path.join(root, file)
			decrypt_file(file_path, key)

# Main program with argparse
def main():
	parser = argparse.ArgumentParser(description="Encrypt, decrypt, or manage encryption keys for files and directories.")

	parser.add_argument("--generate-key", action="store_true", help="Generate a new encryption key.")
	parser.add_argument("--encrypt", action="store_true", help="Encrypt files or a directory.")
	parser.add_argument("--decrypt", action="store_true", help="Decrypt files or a directory.")
	parser.add_argument("--file", type=str, help="Path to a single file to encrypt or decrypt.")
	parser.add_argument("--directory", type=str, help="Path to a directory to encrypt or decrypt.")
	parser.add_argument("--key", type=str, default=DEFAULT_KEY_FILEPATH, help="Path to the encryption key file.")
	parser.add_argument("--password", type=str, help="Password for deriving the encryption key.")
	parser.add_argument("--key-path", type=str, help="Path to save the new key when generating it.")

	args = parser.parse_args()

	if args.generate_key:
		key_filepath = args.key_path or args.key or DEFAULT_KEY_FILEPATH
		generate_key(key_filepath)
		sys.exit(0)

	if not args.encrypt and not args.decrypt:
		parser.error("You must specify either --encrypt or --decrypt.")

	if not args.file and not args.directory:
		parser.error("You must specify either --file or --directory.")

	if args.password:
		salt = secrets.token_bytes(16)  # Generate a unique salt for each password use
		key = derive_key_from_password(args.password, salt)
	elif os.path.isfile(args.key):
		key = load_key(args.key)
	else:
		print(f"Key file '{args.key}' not found.")
		sys.exit(1)

	if args.file:
		if args.encrypt:
			encrypt_file(args.file, key)
		elif args.decrypt:
			decrypt_file(args.file, key)

	if args.directory:
		if not is_safe_directory(args.directory):
			print(f"Processing the directory '{args.directory}' is not allowed for safety reasons.")
			sys.exit(1)
		if args.encrypt:
			encrypt_directory(args.directory, key)
		elif args.decrypt:
			decrypt_directory(args.directory, key)

if __name__ == "__main__":
	main()
