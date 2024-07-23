import os
import sys
from cryptography.fernet import Fernet

# Hardcoded paths for personal use
HARDCODED_KEY_FILEPATH = '/path/to/your/hardcoded/keyfile'
HARDCODED_DIRECTORY_PATH = '/path/to/your/hardcoded/directory'

def load_key(key_filepath):
	"""Load the encryption key from a file."""
	with open(key_filepath, 'rb') as key_file:
		return key_file.read()

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

def confirm_proceed(directory_path):
	"""Confirm with the user before proceeding."""
	print(f"Are you sure you want to encrypt all files in the directory '{directory_path}'? [yes/no]")
	choice = input().strip().lower()
	return choice == 'yes'

def is_safe_directory(directory_path):
	"""Check if the directory is safe to encrypt."""
	unsafe_paths = [os.path.expanduser("~"), "/", "C:\\"]
	return os.path.abspath(directory_path) not in map(os.path.abspath, unsafe_paths)

def main():
	if len(sys.argv) < 2:
		key_filepath = HARDCODED_KEY_FILEPATH
		directory_path = HARDCODED_DIRECTORY_PATH
		skip_confirmation = True
	else:
		key_filepath = sys.argv[1]
		directory_path = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
		skip_confirmation = False

	if not os.path.isfile(key_filepath):
		print(f"Key file '{key_filepath}' not found.")
		sys.exit(1)

	if not os.path.isdir(directory_path):
		print(f"Directory '{directory_path}' not found.")
		sys.exit(1)

	if not is_safe_directory(directory_path):
		print(f"Encryption of the directory '{directory_path}' is not allowed for safety reasons.")
		sys.exit(1)

	if not skip_confirmation and not confirm_proceed(directory_path):
		print("Encryption cancelled by user.")
		sys.exit(1)

	key = load_key(key_filepath)
	fernet = Fernet(key)

	encrypt_directory(directory_path, fernet)

	print(f"All files in '{directory_path}' have been encrypted.")

if __name__ == "__main__":
	main()
