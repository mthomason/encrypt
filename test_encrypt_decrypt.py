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

import unittest
import os
import tempfile
from encryptf import (
	generate_key, load_key, encrypt_data, decrypt_data, encrypt_file, decrypt_file, derive_key_from_password
)

class TestEncryptDecrypt(unittest.TestCase):

	def setUp(self):
		"""Create a temporary directory and files for testing."""
		self.temp_dir = tempfile.TemporaryDirectory()
		self.file_path = os.path.join(self.temp_dir.name, "test_file.txt")
		with open(self.file_path, "w") as file:
			file.write("This is a test file.")
		self.key_path = os.path.join(self.temp_dir.name, "test_key.key")
		self.password = "strongpassword"
		self.salt = b"testsalt12345678"  # 16 bytes for consistency

	def tearDown(self):
		"""Cleanup the temporary directory."""
		self.temp_dir.cleanup()

	def test_generate_and_load_key(self):
		"""Test key generation and loading."""
		generate_key(self.key_path)
		loaded_key = load_key(self.key_path)
		self.assertEqual(len(loaded_key), 32)

	def test_password_derived_key(self):
		"""Test key derivation from a password."""
		key = derive_key_from_password(self.password, self.salt)
		self.assertEqual(len(key), 32)

	def test_encrypt_decrypt_data(self):
		"""Test data encryption and decryption."""
		key = derive_key_from_password(self.password, self.salt)
		original_data = b"Secret message"
		encrypted_data = encrypt_data(original_data, key)
		decrypted_data = decrypt_data(encrypted_data, key)
		self.assertEqual(original_data, decrypted_data)

	def test_encrypt_decrypt_file(self):
		"""Test file encryption and decryption."""
		generate_key(self.key_path)
		key = load_key(self.key_path)

		# Encrypt the file
		encrypt_file(self.file_path, key)

		# Ensure the file content has changed
		with open(self.file_path, "rb") as file:
			encrypted_content = file.read()
		self.assertNotIn(b"This is a test file.", encrypted_content)

		# Decrypt the file
		decrypt_file(self.file_path, key)

		# Verify the file content is restored
		with open(self.file_path, "r") as file:
			decrypted_content = file.read()
		self.assertEqual(decrypted_content, "This is a test file.")

if __name__ == "__main__":
	unittest.main()
