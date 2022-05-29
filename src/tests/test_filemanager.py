from graphsitegen import filesystem
from unittest.mock import MagicMock

from src.graphsitegen.article import ArticleFile

class DiskMock(filesystem.Disk):
    def __init__(self) -> None:
        super().__init__()
        
    def get_files_recursive(self, path):
        return ['file1.md', 'file2.md']

class TestFileManager:

    def setup_method(self, method):
        self.fm = filesystem.FileManager('input', 'output', 'templates')
        self.file = ArticleFile('test', 'input/test.md', 'output/test.html')

    def test_WhenCreateArticleFile_ThenReturnsValidArticleFile(self):
        article = self.fm.create_article_file('test')
        assert article.name == 'test'
        assert article.source == 'input/test.md'
        assert article.output == 'output/test.html'

    def test_WhenCreationTemplateFile_ThenReturnsValidTemplateFile(self):
        template = self.fm.create_template_file('test', 'test_template.html')
        assert template.name == 'test'
        assert template.source == 'templates/test_template.html'
        assert template.output == 'output/test.html'
        assert template.is_template

    def test_WithNoFilter_WhenApplyFilter_ReturnsTrue(self):
        self.fm.file_filters = []
        assert self.fm.apply_filter('test') == True

    def test_WithMatchingFilter_WhenApplyingFilter_ThenReturnsFalse(self):
        self.fm.file_filters = ['test']
        assert self.fm.apply_filter('test') == False

    def test_WithNonMatchingFilter_WhenApplyingFilter_ThenReturnsFalse(self):
        self.fm.file_filters = ['other']
        assert self.fm.apply_filter('test') == True

    def test_WithMockedDisk_WhenListSource_ThenReturnsValidArticleFiles(self):
        self.fm.disk = DiskMock()
        result = self.fm.list_source()
        assert len(result) == 2
        assert result[0].name == 'file1'
        assert result[0].source == 'input/file1.md'
        assert result[0].output == 'output/file1.html'

    def test_WhenExists_ThenDiskIsCalledWithValidPath(self):
        self.fm.disk.file_exists = MagicMock()
        self.fm.exists('test')
        self.fm.disk.file_exists.assert_called_with('input/test.md')

    def test_WithInexistantFile_WhenGetSourceContent_ReturnsEmptyString(self):
        self.fm.disk.file_exists = MagicMock(return_value=False)
        assert self.fm.get_source_content(self.file) == ['']

    def test_WhenGetSourceContent_ThenCorrectFileIsCalled(self):
        self.fm.disk.file_exists = MagicMock(return_value=True)
        self.fm.disk.read_file = MagicMock()
        self.fm.get_source_content(self.file)
        self.fm.disk.read_file.assert_called_with('input/test.md')

    def test_WhenSetSourceContent_ThenCorrectFileIsSet(self):
        self.fm.disk.write_to_file = MagicMock()
        self.fm.set_source_content(self.file, 'hello')
        self.fm.disk.write_to_file.assert_called_with('input/test.md', 'hello')

    def test_WhenSaveOutput_ThenCorrectFileIsSet(self):
        self.fm.disk.write_to_file = MagicMock()
        self.fm.save_output(self.file, 'hello')
        self.fm.disk.write_to_file.assert_called_with('output/test.html', 'hello')

    def test_WhenSaveOutput_ThenDatabaseIsUpdated(self):
        self.fm.disk.write_to_file = MagicMock()
        self.fm.state_monitor.update = MagicMock()
        self.fm.save_output(self.file, 'hello')
        self.fm.state_monitor.update.assert_called_with(self.file)

    def test_WithExistingFile_WhenDeleteArticle_ThenFileIsDeleted(self):
        self.fm.disk.file_exists = MagicMock(return_value=True)
        self.fm.disk.remove_file = MagicMock()
        self.fm.delete_article(self.file)
        self.fm.disk.remove_file.assert_called()

    def test_WhenDeleteArticle_ThenDatabaseIsUpdated(self):
        self.fm.disk.file_exists = MagicMock(return_value=False)
        self.fm.disk.remove_file = MagicMock()
        self.fm.state_monitor.remove = MagicMock()
        self.fm.delete_article(self.file)
        self.fm.state_monitor.remove.assert_called_with(self.file)

