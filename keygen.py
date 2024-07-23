import sys
from cryptography.fernet import Fernet

def generate_key(key_filepath):
	"""Generate and save the encryption key to a file."""
	key = Fernet.generate_key()
	with open(key_filepath, 'wb') as key_file:
		key_file.write(key)
	print(f"Key has been generated and saved to '{key_filepath}'")

def main():
	if len(sys.argv) < 2:
		print("Usage: python generate_key.py <key_filepath>")
		sys.exit(1)

	key_filepath = sys.argv[1]

	generate_key(key_filepath)

if __name__ == "__main__":
	main()
