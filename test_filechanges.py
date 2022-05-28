import pytest
import filechanges
import os
from unittest.mock import MagicMock

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

class TestFileStateGetter:
	def test_WithEmptyFile_WhenComputingHash_ReturnsEmpty(self):
		assert filechanges.FileStateGetter().compute_hash("NotExisting.test") == ""

	def test_WithNonExistingFile_WhenCheckingForExistance_ThenReturnsFalse(self):
		assert filechanges.FileStateGetter().exists("NotExisting.test") == False

class TestFileStateDatabase:
	def test_WhenUpdatingDatabase_ThenPersistenceIsUpdated(self):
		p = FileStateDatabasePersistenceMemory()
		db = filechanges.FileStateDatabase(p)
		db.update('Test', filechanges.FileState("Test.md", "Test.html", "ABCD", "EFGH"))
		assert "Test" in p.states

	def test_WithEmptyDatabase_WhenGetting_ThenThrowsException(self):
		db = filechanges.FileStateDatabase(FileStateDatabasePersistenceMemory())
		with pytest.raises(Exception) as e_info:
			assert db.get("none.md") == None
	
	def test_WithEmptyDatabase_WhenTestingIfItemExists_ThenReturnsFalse(self):
		db = filechanges.FileStateDatabase(FileStateDatabasePersistenceMemory())
		assert db.exists("no.md") == False

	def test_WithExistingEntryInDb_WhenRemovingItem_ThenDatabaseRemovesEntry(self):
		p = FileStateDatabasePersistenceMemory()
		p.states['SomeFile.md'] = filechanges.FileStateGetter().get("SomeFile.md", "SomeOutput.html")
		db = filechanges.FileStateDatabase(p)
		db.remove("SomeFile.md")
		assert 'SomeFile.md' not in p.states

	def test_WithTwoExistingEntries_WhenGettingDeleted_ThenSecondEntryIsReturned(self):
		p = FileStateDatabasePersistenceMemory()
		p.states['file1.md'] = filechanges.FileState('file1.md', '', '', '')
		p.states['file2.md'] = filechanges.FileState('file2.md', '', '', '')
		db = filechanges.FileStateDatabase(p)
		result = db.get_deleted(['file1.md'])
		assert len(result) == 1
		assert result[0] == 'file2.md'
		assert db.exists('file1.md') == True
		assert db.exists('file2.md') == True

	def test_WhenRemovingEntry_ThenFileSystemIsUpdated(self):
		p = FileStateDatabasePersistenceMemory()
		p.save = MagicMock()
		db = filechanges.FileStateDatabase(p)
		db.states['test'] = filechanges.FileState('test.md', '', '', '')
		db.remove('test')
		p.save.assert_called_with(db.states)
		assert db.exists('test') == False

class TestFileStateMonitor:

	class FileStateDatabaseMock(filechanges.FileStateDatabase):
		def __init__(self) -> None:
			self.states = {}

		def exists(self, name):
			return name in self.states

		def get(self, name):
			return self.states[name]

		def update(self, name, state):
			self.states[name] = state

		def remove(self, name):
			del self.states[name]

	def test_WithEmptyDatabase_WhenHasChanged_ThenReturnsTrue(self):
		db = TestFileStateMonitor.FileStateDatabaseMock()
		mon = filechanges.FileStateMonitor(db, "dest")
		assert mon.has_changed("Unexisting") == True

	def test_WithExistingFile_WhenHasNotChanged_ThenReturnsFalse(self):
		state = filechanges.FileState('file.md', 'file.html', 'abcd', 'abcd')
		db = TestFileStateMonitor.FileStateDatabaseMock()
		db.exists = MagicMock(return_value=True)
		db.get = MagicMock(return_value=state)
		mon = filechanges.FileStateMonitor(db, "dest")
		mon.state_getter.get = MagicMock(return_value=state)
		assert mon.has_changed('file.md') == False

	def test_WithExistingFile_WhenHasChanged_ThenReturnsTrue(self):
		prev_state = filechanges.FileState('file.md', 'file.html', 'abcd', 'abcd')
		current_state = filechanges.FileState('file.md', 'file.html', 'abcde', 'abcdf')
		db = TestFileStateMonitor.FileStateDatabaseMock()
		db.exists = MagicMock(return_value=True)
		db.get = MagicMock(return_value=prev_state)
		mon = filechanges.FileStateMonitor(db, "dest")
		mon.state_getter.get = MagicMock(return_value=current_state)
		assert mon.has_changed('file.md') == True

	def test_WithExistingFile_WhenSourceHasChanged_ThenReturnsTrue(self):
		prev_state = filechanges.FileState('file.md', 'file.html', 'abcd', 'abcd')
		current_state = filechanges.FileState('file.md', 'file.html', 'abcde', 'abcd')
		db = TestFileStateMonitor.FileStateDatabaseMock()
		db.exists = MagicMock(return_value=True)
		db.get = MagicMock(return_value=prev_state)
		mon = filechanges.FileStateMonitor(db, "dest")
		mon.state_getter.get = MagicMock(return_value=current_state)
		assert mon.has_changed('file.md') == True

	def test_WithExistingFile_WhenDestinationHasChanged_ThenReturnsTrue(self):
		prev_state = filechanges.FileState('file.md', 'file.html', 'abcd', 'abcd')
		current_state = filechanges.FileState('file.md', 'file.html', 'abcd', 'abcdf')
		db = TestFileStateMonitor.FileStateDatabaseMock()
		db.exists = MagicMock(return_value=True)
		db.get = MagicMock(return_value=prev_state)
		mon = filechanges.FileStateMonitor(db, "dest")
		mon.state_getter.get = MagicMock(return_value=current_state)
		assert mon.has_changed('file.md') == True

	def test_WithEmptyDatabase_WhenUpdate_ThenUpdatesDatabase(self):
		db = TestFileStateMonitor.FileStateDatabaseMock()
		mon = filechanges.FileStateMonitor(db, "dest")
		mon.update('unexisting-file', "unexisting-file.md")
		assert db.exists("unexisting-file") == True

	def test_WithFileInDatabase_WithInexistantFile_WhenUpdate_ThenFileGetsRemovedFromDatabase(self):
		db = TestFileStateMonitor.FileStateDatabaseMock()
		db.exists = MagicMock(return_value=True)
		db.remove = MagicMock()
		mon = filechanges.FileStateMonitor(db, 'dest')
		mon.update('some-inexistant-file', 'some-inexistant-file.md')
		db.remove.assert_called_with('some-inexistant-file')

	def test_WithFileSystemFile_WhenGettingDestination_ThenReturnsValidDestination(self):
		mon = filechanges.FileStateMonitor(TestFileStateMonitor.FileStateDatabaseMock(), '.')
		with open('test-file.md', 'w') as f:
			f.write('.')
		with open('test-file.html', 'w') as f2:
			f2.write('.')
		dest = mon.get_destination('./test-file.md')
		os.path.isfile(dest)
		os.remove('./test-file.md')
		os.remove('./test-file.html')

	def test_WithTwoFiles_WithOneDeleted_WhenGettingChangedFiles_ThenDeletedFileIsReturned(self):
		db = TestFileStateMonitor.FileStateDatabaseMock()
		db.states['file1.md'] = filechanges.FileState('file1.md', '', '', '')
		db.states['file2.md'] = filechanges.FileState('file2.md', '', '', '')
		mon = filechanges.FileStateMonitor(db, '')
		changed = mon.get_changed_files(['file1.md'])
		assert len(changed) == 1
		assert changed[0] == 'file2.md'

	def mock_has_changed(self, file):
		return file == 'file3.md'

	def test_WithThreeFiles_WithOneDeleted_WithOneChanged_WhenGettingChangedFiles_ThenDeletedFileAndChangedFileIsReturned(self):
		db = TestFileStateMonitor.FileStateDatabaseMock()
		db.states['file1.md'] = filechanges.FileState('file1.md', '', 'abc', '')
		db.states['file2.md'] = filechanges.FileState('file2.md', '', 'abc', '')
		db.states['file2.md'] = filechanges.FileState('file3.md', '', 'abc', '')
		mon = filechanges.FileStateMonitor(db, '')
		mon.has_changed = MagicMock(side_effect=self.mock_has_changed)
		changed = mon.get_changed_files(['file1.md', 'file3.md'])
		assert len(changed) == 2
		assert changed[0] == 'file2.md'
		assert changed[1] == 'file3.md'

		