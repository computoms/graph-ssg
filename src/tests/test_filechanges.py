import pytest
import os
from unittest.mock import MagicMock
from graphsitegen.article import ArticleFile
from graphsitegen.filesystem import filechanges

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
		states['Test.md'] = filechanges.FileState('Test', "Test.md", "Test.html", "ASBD", "SLKD")
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

	def setup_method(self, method):
		self.db = filechanges.FileStateDatabase(FileStateDatabasePersistenceMemory())

	def test_WhenUpdatingDatabase_ThenPersistenceIsUpdated(self):
		self.db.update('Test', filechanges.FileState('Test', "Test.md", "Test.html", "ABCD", "EFGH"))
		assert "Test" in self.db.persistence.states

	def test_WithEmptyDatabase_WhenGetting_ThenThrowsException(self):
		with pytest.raises(Exception) as e_info:
			assert self.db.get("none.md") == None
	
	def test_WithEmptyDatabase_WhenTestingIfItemExists_ThenReturnsFalse(self):
		assert self.db.exists("no.md") == False

	def test_WithExistingEntryInDb_WhenRemovingItem_ThenDatabaseRemovesEntry(self):
		self.db.persistence.states['SomeFile.md'] = filechanges.FileStateGetter().get('SomeFile', "SomeFile.md", "SomeOutput.html")
		self.db.remove("SomeFile.md")
		assert 'SomeFile.md' not in self.db.persistence.states

	def test_WithTwoExistingEntries_WhenGettingDeleted_ThenSecondEntryIsReturned(self):
		self.db.persistence.states['file1.md'] = filechanges.FileState('file1', 'file1.md', '', '', '')
		self.db.persistence.states['file2.md'] = filechanges.FileState('file2', 'file2.md', '', '', '')
		result = self.db.get_deleted_states(['file1.md'])
		assert len(result) == 1
		assert result[0].source == 'file2.md'
		assert self.db.exists('file1.md') == True
		assert self.db.exists('file2.md') == True

	def test_WhenRemovingEntry_ThenFileSystemIsUpdated(self):
		self.db.persistence.save = MagicMock()
		self.db.states['test'] = filechanges.FileState('test', 'test.md', '', '', '')
		self.db.remove('test')
		self.db.persistence.save.assert_called_with(self.db.states)
		assert self.db.exists('test') == False

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

	def setup_method(self, method):
		self.db = TestFileStateMonitor.FileStateDatabaseMock()
		self.mon = filechanges.FileStateMonitor(self.db, 'dest')
		self.state = self.make_filestate('file')

	def make_filestate(self, name):
		return filechanges.FileState(name, name + '.md', name + '.html', '', '')

	def test_WithEmptyDatabase_WhenHasChanged_ThenReturnsTrue(self):
		assert self.mon.has_changed(ArticleFile('Unchanged', '', '')) == True

	def test_WithExistingFile_WhenHasNotChanged_ThenReturnsFalse(self):
		self.db.exists = MagicMock(return_value=True)
		self.db.get = MagicMock(return_value=self.state)
		self.mon.state_getter.get = MagicMock(return_value=self.state)
		assert self.mon.has_changed(ArticleFile('file', 'file.md', 'file.html')) == False

	def test_WithExistingFile_WhenHasChanged_ThenReturnsTrue(self):
		current_state = filechanges.FileState('file', 'file.md', 'file.html', 'abcde', 'abcdf')
		self.db.exists = MagicMock(return_value=True)
		self.db.get = MagicMock(return_value=self.state)
		self.mon.state_getter.get = MagicMock(return_value=current_state)
		assert self.mon.has_changed(ArticleFile('file', 'file.md', 'file.html')) == True

	def test_WithExistingFile_WhenSourceHasChanged_ThenReturnsTrue(self):
		current_state = filechanges.FileState('file', 'file.md', 'file.html', 'abcde', '')
		self.db.exists = MagicMock(return_value=True)
		self.db.get = MagicMock(return_value=self.state)
		self.mon.state_getter.get = MagicMock(return_value=current_state)
		assert self.mon.has_changed(ArticleFile('file', '', '')) == True

	def test_WithExistingFile_WhenDestinationHasChanged_ThenReturnsTrue(self):
		current_state = filechanges.FileState('file', 'file.md', 'file.html', '', 'abcdf')
		self.db.exists = MagicMock(return_value=True)
		self.db.get = MagicMock(return_value=self.state)
		self.mon.state_getter.get = MagicMock(return_value=current_state)
		assert self.mon.has_changed(ArticleFile('file', 'file.md', 'file.html')) == True

	def test_WithEmptyDatabase_WhenUpdate_ThenUpdatesDatabase(self):
		self.mon.update(ArticleFile('file', 'file.md', 'file.html'))
		assert self.db.exists('file') == True

	def test_WithTemplate_WhenUpdate_ThenDoesNotUpdateDatabase(self):
		file = ArticleFile('template', 'template.md', 'template.html')
		file.is_template = True
		self.mon.update(file)
		assert self.db.exists('template') == False
	
	def test_WithExistingTemplate_WhenHasChanged_ThenAlwaysTrue(self):
		file = ArticleFile('template', 'template.md', 'template.html')
		self.mon.update(file)
		file.is_template = True
		assert self.mon.has_changed(file) == True

	def test_WithFileInDatabase_WithInexistantFile_WhenUpdate_ThenFileGetsRemovedFromDatabase(self):
		self.db.exists = MagicMock(return_value=True)
		self.db.remove = MagicMock()
		self.mon.update(ArticleFile('file', 'file.md', 'file.html'))
		self.db.remove.assert_called_with('file')

	def test_WithTwoFiles_WithOneDeleted_WhenGettingChangedFiles_ThenDeletedFileIsReturned(self):
		self.db.states['file1'] = self.make_filestate('file1')
		self.db.states['file2'] = self.make_filestate('file2')
		changed = self.mon.get_changed_files([ArticleFile('file1', 'file1.md', '')])
		assert len(changed) == 1
		assert changed[0].source == 'file2.md'

	def mock_has_changed(self, file):
		return file.name == 'file3'

	def test_WithThreeFiles_WithOneDeleted_WithOneChanged_WhenGettingChangedFiles_ThenDeletedFileAndChangedFileIsReturned(self):
		self.db.states['file1'] = self.make_filestate('file1')
		self.db.states['file2'] = self.make_filestate('file2')
		self.db.states['file3'] = self.make_filestate('file3')
		self.mon.has_changed = MagicMock(side_effect=self.mock_has_changed)
		changed = self.mon.get_changed_files([ArticleFile('file1', 'file1.md', ''), ArticleFile('file3', 'file3.md', '')])
		assert len(changed) == 2
		assert changed[0].name == 'file2'
		assert changed[1].name == 'file3'

		