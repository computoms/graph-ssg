import hashlib
import os

class FileChangeRegister:
	def __init__(self, database_file):
		self.change_db = database_file
		if not os.path.isfile(database_file):
			with open(database_file, "w") as file:
				file.write("\n")

	def read_registers(self):
		registers = {}
		with open(self.change_db, "r") as file:
			lines = file.readlines()
			for line in lines:
				s = line.split(',')
				if (len(s) > 1):
					registers[s[0]] = s[1]
		return registers

	def write_registers(self, registers):
		csv_content = ""
		for k in registers:
			csv_content += k + "," + registers[k] + "\n"

		with open(self.change_db, "w") as file:
			file.write(csv_content)

	def compute_hash(self, filename):
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
			registers[filename] = new_hash
			self.write_registers(registers)
			return True