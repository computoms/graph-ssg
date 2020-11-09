import filechanges
import os

def readregisters_whenemptyfile_returnsemptycollection():
	with open("test/empty.txt", "w") as file:
		file.write("\n")
	r = filechanges.FileChangeRegister("test/empty.txt")

	registers = r.read_registers()
	assert(len(registers) == 0)
	os.remove("test/empty.txt")

def readregisters_whensingleentry_returnscorrectentry():
	with open("test/single.txt", "w") as file:
		file.write("TestFile.txt,ABCDE\n")
	r2 = filechanges.FileChangeRegister("test/single.txt")
	regs = r2.read_registers()
	assert(len(regs) == 1)
	assert(regs['TestFile.txt'].rstrip() == 'ABCDE')
	os.remove("test/single.txt")


def writeregisters_whensingleentry_writescorrectfile():
	registers = {}
	registers['TestFile.txt'] = 'ABCDE'
	r = filechanges.FileChangeRegister("test/single.txt")
	r.write_registers(registers)
	with open("test/single.txt", "r") as file:
		lines = file.readlines()
		assert(len(lines) == 1)
		assert(lines[0].rstrip() == "TestFile.txt,ABCDE")
	os.remove("test/single.txt")

def haschanged_whenfilenotchanged_returnsfalse():
	r = filechanges.FileChangeRegister("test/nochange.txt")
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello")
	with open("test/nochange.txt", "w") as file:
		file.write("test/TestFile.txt," + r.compute_hash("test/TestFile.txt") + "\n")
	
	assert(r.has_changed("test/TestFile.txt") == False)
	os.remove("test/TestFile.txt")
	os.remove("test/nochange.txt")

def haschanged_whenfilechanged_returnstrue():
	r = filechanges.FileChangeRegister("test/change.txt")
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello")
	with open("test/change.txt", "w") as file:
		file.write("test/TestFile.txt," + r.compute_hash("test/TestFile.txt") + "\n")
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello2")
	
	assert(r.has_changed("test/TestFile.txt") == True)
	os.remove("test/TestFile.txt")
	os.remove("test/change.txt")

def haschanged_whenfilenotinregister_addstoregister():
	r = filechanges.FileChangeRegister("test/change.txt")
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello")
	with open("test/change.txt", "w") as file:
		file.write("\n")
	assert(r.has_changed("test/TestFile.txt") == True)
	with open("test/change.txt", "r") as file:
		lines = file.readlines()
		assert(len(lines) == 1)
		content = "test/TestFile.txt," + r.compute_hash("test/TestFile.txt")
		assert(lines[0].rstrip() == content)
	os.remove("test/TestFile.txt")
	os.remove("test/change.txt")

def update_whenfileinregister_updatesregister():
	r = filechanges.FileChangeRegister("test/change.txt")
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello")
	with open("test/change.txt", "w") as file:
		file.write("test/TestFile.txt," + r.compute_hash("test/TestFile.txt") + "\n")
	assert(r.has_changed("test/TestFile.txt") == False)
	with open("test/TestFile.txt", "w") as file:
		file.write("Hello 2")
	assert(r.has_changed("test/TestFile.txt") == True)
	r.update("test/TestFile.txt")
	assert(r.has_changed("test/TestFile.txt") == False)
	os.remove("test/TestFile.txt")
	os.remove("test/change.txt")


readregisters_whenemptyfile_returnsemptycollection()
readregisters_whensingleentry_returnscorrectentry()
writeregisters_whensingleentry_writescorrectfile()
haschanged_whenfilenotchanged_returnsfalse()
haschanged_whenfilechanged_returnstrue()
haschanged_whenfilenotinregister_addstoregister()
update_whenfileinregister_updatesregister()