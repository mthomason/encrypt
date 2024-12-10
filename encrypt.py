import os
import sys
import argparse
from cryptography.fernet import Fernet, InvalidToken

# Default key file location
DEFAULT_KEY_FILEPATH = os.path.expanduser("~/.encryption_key")

# Functions shared between operations
def load_key(key_filepath):
	"""Load the encryption key from a file."""
	with open(key_filepath, 'rb') as key_file:
		return key_file.read()

def generate_key(key_filepath):
	"""Generate and save a new encryption key."""
	key = Fernet.generate_key()
	with open(key_filepath, 'wb') as key_file:
		key_file.write(key)
	print(f"Key has been generated and saved to '{key_filepath}'")

def is_safe_directory(directory_path):
	"""Check if the directory is safe to process."""
	unsafe_paths = [os.path.expanduser("~"), "/", "C:\\"]
	return os.path.abspath(directory_path) not in map(os.path.abspath, unsafe_paths)

# Encryption functions
def encrypt_file(file_path, fernet):
	"""Encrypt a single file."""
	try:
		with open(file_path, 'rb') as file:
			data = file.read()
		encrypted_data = fernet.encrypt(data)
		with open(file_path, 'wb') as file:
			file.write(encrypted_data)
		print(f"Encrypted: {file_path}")
	except Exception as e:
		print(f"Failed to encrypt {file_path}: {e}")

def encrypt_directory(directory_path, fernet):
	"""Encrypt all files in the specified directory."""
	for root, _, files in os.walk(directory_path):
		for file in files:
			file_path = os.path.join(root, file)
			encrypt_file(file_path, fernet)

# Decryption functions
def decrypt_file(file_path, fernet):
	"""Decrypt a single file."""
	try:
		with open(file_path, 'rb') as file:
			encrypted_data = file.read()
		try:
			decrypted_data = fernet.decrypt(encrypted_data)
		except InvalidToken:
			print(f"Invalid token for file: {file_path}")
			return
		with open(file_path, 'wb') as file:
			file.write(decrypted_data)
		print(f"Decrypted: {file_path}")
	except Exception as e:
		print(f"Failed to decrypt {file_path}: {e}")

def decrypt_directory(directory_path, fernet):
	"""Decrypt all files in the specified directory."""
	for root, _, files in os.walk(directory_path):
		for file in files:
			file_path = os.path.join(root, file)
			decrypt_file(file_path, fernet)

# Main program with argparse
def main():
	parser = argparse.ArgumentParser(description="Encrypt, decrypt, or manage encryption keys for files and directories.")
	
	parser.add_argument("--generate-key", action="store_true", help="Generate a new encryption key.")
	parser.add_argument("--encrypt", action="store_true", help="Encrypt files or a directory.")
	parser.add_argument("--decrypt", action="store_true", help="Decrypt files or a directory.")
	parser.add_argument("--file", type=str, help="Path to a single file to encrypt or decrypt.")
	parser.add_argument("--directory", type=str, help="Path to a directory to encrypt or decrypt.")
	parser.add_argument("--key", type=str, default=DEFAULT_KEY_FILEPATH, help="Path to the encryption key file.")

	args = parser.parse_args()

	if args.generate_key:
		key_filepath = args.key or DEFAULT_KEY_FILEPATH
		generate_key(key_filepath)
		sys.exit(0)

	if not args.encrypt and not args.decrypt:
		parser.error("You must specify either --encrypt or --decrypt.")

	if not args.file and not args.directory:
		parser.error("You must specify either --file or --directory.")

	if not os.path.isfile(args.key):
		print(f"Key file '{args.key}' not found.")
		sys.exit(1)

	key = load_key(args.key)
	fernet = Fernet(key)

	if args.file:
		if args.encrypt:
			encrypt_file(args.file, fernet)
		elif args.decrypt:
			decrypt_file(args.file, fernet)

	if args.directory:
		if not is_safe_directory(args.directory):
			print(f"Processing the directory '{args.directory}' is not allowed for safety reasons.")
			sys.exit(1)
		if args.encrypt:
			encrypt_directory(args.directory, fernet)
		elif args.decrypt:
			decrypt_directory(args.directory, fernet)

if __name__ == "__main__":
	main()
