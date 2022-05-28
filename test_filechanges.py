import filechanges
import os

# Mock of IO to disk
class MemoryFile(filechanges.File):
	def __init__(self, lines) -> None:
		super().__init__("")
		self.lines = lines

	def get_lines(self):
		return self.lines

	def write_content(self, content):
		self.lines = content.split('\n')

	def assert_file(self):
		pass

def init():
	if not os.path.isdir("test"):
		os.mkdir("test")

def test_WithEmptyFile_WhenReadingRegisters_ThenReturnsEmptyCollection():
	init()
	empty_db = MemoryFile([])
	r = filechanges.FileChangeRegister(empty_db)

	registers = r.read_registers()
	assert len(registers) == 0

def test_WithSingleEntry_WhenReadingRegisters_ThenReturnsCorrectEntry():
	init()
	single_db = MemoryFile(["TestFile.txt,ABCDE\n"])
	r2 = filechanges.FileChangeRegister(single_db)
	regs = r2.read_registers()
	assert(len(regs) == 1)
	assert(regs['TestFile.txt'].rstrip() == 'ABCDE')


def test_WithSingleEngty_WhenWritingRegisters_ThenWritesCorrectFile():
	init()
	registers = {}
	registers['TestFile.txt'] = 'ABCDE'
	db = MemoryFile([])
	r = filechanges.FileChangeRegister(db)
	r.write_registers(registers)
	assert(len(db.get_lines()) == 2)
	assert(db.get_lines()[0] == "TestFile.txt,ABCDE")

def test_WithUnchangedFile_WhenHasChanged_ThenReturnsFalse():
	init()
	db = MemoryFile([])
	r = filechanges.FileChangeRegister(db)
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello")
	db.write_content("test/TestFile.txt," + r.compute_hash("test/TestFile.txt") + "\n")
	
	assert(r.has_changed("test/TestFile.txt") == False)
	os.remove("test/TestFile.txt")

def test_WithChangedFile_WhenHasChanged_ThenReturnsTrue():
	init()
	db = MemoryFile([])
	r = filechanges.FileChangeRegister(db)
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello")
	db.write_content("test/TestFile.txt," + r.compute_hash("test/TestFile.txt") + "\n")
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello2")
	
	assert(r.has_changed("test/TestFile.txt") == True)
	os.remove("test/TestFile.txt")

def test_WithFileNotInRegister_WhenHasChanged_ThenAddsToRegister():
	init()
	db = MemoryFile([])
	r = filechanges.FileChangeRegister(db)
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello")
	assert(r.has_changed("test/TestFile.txt") == True)
	assert(len(r.read_registers()) == 1)
	assert(r.read_registers()["test/TestFile.txt"] == r.compute_hash("test/TestFile.txt"))
	os.remove("test/TestFile.txt")

def test_WithFileInRegister_WhenUpdate_ThenUpdatesRegister():
	init()
	db = MemoryFile([])
	r = filechanges.FileChangeRegister(db)
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello")
	db.write_content("test/TestFile.txt," + r.compute_hash("test/TestFile.txt") + "\n")
	assert(r.has_changed("test/TestFile.txt") == False)
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello 2")
	assert(r.has_changed("test/TestFile.txt") == True)
	r.update("test/TestFile.txt")
	assert(r.has_changed("test/TestFile.txt") == False)
	os.remove("test/TestFile.txt")