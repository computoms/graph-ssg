import pytest
import filechanges
import os

# Persistence of file states into memory
class FileStateDatabasePersistenceMemory(filechanges.FileStateDatabasePersistence):
	def __init__(self) -> None:
		super().__init__("")
		self.states = {}

	def save(self, states):
		self.states = states

	def load(self):
		return self.states

class TestDatabasePersistenceFile:
	def test_WithOneState_WhenSavingThenLoading_ThenGivesCorrectStates(self):
		persistence = filechanges.FileStateDatabasePersistence("test.json")
		states = {}
		states['Test.md'] = filechanges.FileState("Test.md", "Test.html", "ASBD", "SLKD")
		persistence.save(states)
		states2 = persistence.load()
		assert 'Test.md' in states2
		assert states2['Test.md'].source == 'Test.md'
		assert states2['Test.md'].destination == 'Test.html'
		assert states2['Test.md'].source_hash == 'ASBD'
		assert states2['Test.md'].destination_hash == 'SLKD'
		os.remove("test.json")

	def test_WithUnexistingDatabaseFile_WhenLoading_ReturnsEmptyDatabase(self):
		p = filechanges.FileStateDatabasePersistence("test.json")
		db = p.load()
		assert len(db) == 0

class TestFileState:
	def test_WithEmptyFile_WhenComputingHash_ReturnsEmpty(self):
		assert filechanges.FileState.compute_hash("NotExisting.test") == ""

class TestFileStateDatabase:
	def test_WhenUpdatingDatabase_ThenPersistenceIsUpdated(self):
		p = FileStateDatabasePersistenceMemory()
		db = filechanges.FileStateDatabase(p)
		db.update(filechanges.FileState("Test.md", "Test.html", "ABCD", "EFGH"))
		assert "Test.md" in p.states

	def test_WithEmptyDatabase_WhenGetting_ThenThrowsException(self):
		p = FileStateDatabasePersistenceMemory()
		db = filechanges.FileStateDatabase(p)
		with pytest.raises(Exception) as e_info:
			assert db.get("none.md") == None
	
	def test_WithEmptyDatabase_WhenTestingIfItemExists_ThenReturnsFalse(self):
		p = FileStateDatabasePersistenceMemory()
		db = filechanges.FileStateDatabase(p)
		assert db.exists("no.md") == False

class TestFileStateMonitor:
	def test_WithEmptyDatabase_WhenHasChanged_ThenReturnsTrue(self):
		p = FileStateDatabasePersistenceMemory()
		db = filechanges.FileStateDatabase(p)
		mon = filechanges.FileStateMonitor(db, "dest")
		assert mon.has_changed("Unexisting") == True

	def test_WithExistingFile_WhenHasNotChanged_ThenReturnsFalse(self):
		p = FileStateDatabasePersistenceMemory()
		db = filechanges.FileStateDatabase(p)
		db.update(filechanges.FileState("unexisting-file.md", "unexisting-file.html", "", ""))
		mon = filechanges.FileStateMonitor(db, "dest")
		assert mon.has_changed("unexisting-file.md") == False

	def test_WithExistingFile_WhenSourceHasChanged_ThenReturnsTrue(self):
		p = FileStateDatabasePersistenceMemory()
		db = filechanges.FileStateDatabase(p)
		db.update(filechanges.FileState("unexisting-file.md", "unexisting-file.html", "ABCD", ""))
		mon = filechanges.FileStateMonitor(db, "dest")
		assert mon.has_changed("unexisting-file.md") == True

	def test_WithExistingFile_WhenDestinationHasChanged_ThenReturnsTrue(self):
		p = FileStateDatabasePersistenceMemory()
		db = filechanges.FileStateDatabase(p)
		db.update(filechanges.FileState("unexisting-file.md", "unexisting-file.html", "", "ABCD"))
		mon = filechanges.FileStateMonitor(db, "dest")
		assert mon.has_changed("unexisting-file.md") == True

	def test_WithEmptyDatabase_WhenUpdate_ThenUpdatesDatabase(self):
		p = FileStateDatabasePersistenceMemory()
		db = filechanges.FileStateDatabase(p)
		mon = filechanges.FileStateMonitor(db, "dest")
		mon.update("unexisting-file.md")
		assert db.exists("unexisting-file.md") == True