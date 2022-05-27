import hashlib
import os

# IO Access to disk
class File:
	def __init__(self, path):
		self.path = path

	def get_lines(self):
		with open(self.path, "r") as file:
			return file.readlines()

	def write_content(self, content):
		with open(self.path, "w") as file:
			file.write(content)

	def assert_file(self):
		if not os.path.isfile(self.path):
			with open(self.path, "w") as file:
				file.write("\n")

# Handles file change monitoring
class FileChangeRegister:
	def __init__(self, change_database):
		# Generate unique name based on outputFolder to register the file changes
		self.change_db = change_database
		self.change_db.assert_file()

	def read_registers(self):
		registers = {}
		lines = self.change_db.get_lines()
		for line in lines:
			s = line.split(',')
			if (len(s) > 1):
				registers[s[0]] = s[1]
		return registers

	def write_registers(self, registers):
		csv_content = ""
		for k in registers:
			csv_content += k + "," + registers[k] + "\n"

		self.change_db.write_content(csv_content)

	def compute_hash(self, filename):
		if not os.path.exists(filename):
			return ""
		return hashlib.md5(open(filename,'rb').read()).hexdigest()

	def update(self, filename):
		registers = self.read_registers()
		registers[filename] = self.compute_hash(filename)
		self.write_registers(registers)

	def has_changed(self, filename):
		registers = self.read_registers()
		new_hash = self.compute_hash(filename)
		if filename in registers:
			return registers[filename].rstrip() != new_hash
		else:
			self.update(filename)
			return True