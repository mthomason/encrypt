import os
import sys
from cryptography.fernet import Fernet

def load_key(key_filepath):
	"""Load the encryption key from a file."""
	with open(key_filepath, 'rb') as key_file:
		return key_file.read()

def decrypt_file(file_path, fernet):
	"""Decrypt a single file."""
	with open(file_path, 'rb') as file:
		encrypted_data = file.read()

	try:
		decrypted_data = fernet.decrypt(encrypted_data)
	except cryptography.fernet.InvalidToken:
		print(f"Invalid token for file: {file_path}")
		return

	with open(file_path, 'wb') as file:
		file.write(decrypted_data)

def decrypt_directory(directory_path, fernet):
	"""Decrypt all files in the specified directory."""
	for root, _, files in os.walk(directory_path):
		for file in files:
			file_path = os.path.join(root, file)
			decrypt_file(file_path, fernet)

def main():
	if len(sys.argv) < 2:
		print("Usage: python decrypt_files.py <key_filepath> [<directory_path>]")
		sys.exit(1)

	key_filepath = sys.argv[1]
	directory_path = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()

	if not os.path.isfile(key_filepath):
		print(f"Key file '{key_filepath}' not found.")
		sys.exit(1)

	if not os.path.isdir(directory_path):
		print(f"Directory '{directory_path}' not found.")
		sys.exit(1)

	key = load_key(key_filepath)
	fernet = Fernet(key)

	decrypt_directory(directory_path, fernet)

	print(f"All files in '{directory_path}' have been decrypted.")

if __name__ == "__main__":
	main()
