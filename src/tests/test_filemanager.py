from graphsitegen.filesystem.filemanager import FileManager
from graphsitegen.filesystem.filemanager import Disk
from unittest.mock import MagicMock

from src.graphsitegen.article import ArticleFile

class DiskMock(Disk):
    def __init__(self) -> None:
        super().__init__()
        
    def get_files_recursive(self, path):
        return ['file1.md', 'file2.md']

class TestFileManager:
    def test_WhenCreateArticleFile_ThenReturnsValidArticleFile(self):
        fm = FileManager('input', 'output', 'templates')
        article = fm.create_article_file('test')
        assert article.name == 'test'
        assert article.source == 'input/test.md'
        assert article.output == 'output/test.html'

    def test_WhenCreationTemplateFile_ThenReturnsValidTemplateFile(self):
        fm = FileManager('input', 'output', 'templates')
        template = fm.create_template_file('test', 'test_template.html')
        assert template.name == 'test'
        assert template.source == 'templates/test_template.html'
        assert template.output == 'output/test.html'
        assert template.is_template

    def test_WithNoFilter_WhenApplyFilter_ReturnsTrue(self):
        fm = FileManager('intput', 'output', 'templates')
        fm.file_filters = []
        assert fm.apply_filter('test') == True

    def test_WithMatchingFilter_WhenApplyingFilter_ThenReturnsFalse(self):
        fm = FileManager('intput', 'output', 'templates')
        fm.file_filters = ['test']
        assert fm.apply_filter('test') == False

    def test_WithNonMatchingFilter_WhenApplyingFilter_ThenReturnsFalse(self):
        fm = FileManager('intput', 'output', 'templates')
        fm.file_filters = ['other']
        assert fm.apply_filter('test') == True

    def test_WithMockedDisk_WhenListSource_ThenReturnsValidArticleFiles(self):
        fm = FileManager('input', 'output', 'templates')
        fm.disk = DiskMock()
        result = fm.list_source()
        assert len(result) == 2
        assert result[0].name == 'file1'
        assert result[0].source == 'input/file1.md'
        assert result[0].output == 'output/file1.html'

    def test_WhenExists_ThenDiskIsCalledWithValidPath(self):
        fm = FileManager('input', 'output', 'templates')
        fm.disk.file_exists = MagicMock()
        fm.exists('test')
        fm.disk.file_exists.assert_called_with('input/test.md')

    def test_WithInexistantFile_WhenGetSourceContent_ReturnsEmptyString(self):
        fm = FileManager('input', 'output', 'templates')
        fm.disk.file_exists = MagicMock(return_value=False)
        assert fm.get_source_content(ArticleFile('test', 'test.md', 'test.html')) == ['']

    def test_WhenGetSourceContent_ThenCorrectFileIsCalled(self):
        fm = FileManager('input', 'output', 'templates')
        fm.disk.file_exists = MagicMock(return_value=True)
        fm.disk.read_file = MagicMock()
        fm.get_source_content(ArticleFile('test', 'input/test.md', 'output/test.html'))
        fm.disk.read_file.assert_called_with('input/test.md')

    def test_WhenSetSourceContent_ThenCorrectFileIsSet(self):
        fm = FileManager('input', 'output', 'templates')
        fm.disk.write_to_file = MagicMock()
        fm.set_source_content(ArticleFile('test', 'input/test.md', 'output/test.html'), 'hello')
        fm.disk.write_to_file.assert_called_with('input/test.md', 'hello')

    def test_WhenSaveOutput_ThenCorrectFileIsSet(self):
        fm = FileManager('input', 'output', 'templates')
        fm.disk.write_to_file = MagicMock()
        fm.save_output(ArticleFile('test', 'input/test.md', 'output/test.html'), 'hello')
        fm.disk.write_to_file.assert_called_with('output/test.html', 'hello')

    def test_WhenSaveOutput_ThenDatabaseIsUpdated(self):
        fm = FileManager('input', 'output', 'templates')
        fm.disk.write_to_file = MagicMock()
        fm.state_monitor.update = MagicMock()
        file = ArticleFile('test', 'input/test.md', 'output/test.html')
        fm.save_output(file, 'hello')
        fm.state_monitor.update.assert_called_with(file)

    def test_WithExistingFile_WhenDeleteArticle_ThenFileIsDeleted(self):
        fm = FileManager('input', 'output', 'templates')
        fm.disk.file_exists = MagicMock(return_value=True)
        fm.disk.remove_file = MagicMock()
        file = ArticleFile('test', 'input/test.md', 'output/test.html')
        fm.delete_article(file)
        fm.disk.remove_file.assert_called()

    def test_WhenDeleteArticle_ThenDatabaseIsUpdated(self):
        fm = FileManager('input', 'output', 'templates')
        fm.disk.file_exists = MagicMock(return_value=False)
        fm.disk.remove_file = MagicMock()
        fm.state_monitor.remove = MagicMock()
        file = ArticleFile('test', 'input/test.md', 'output/test.html')
        fm.delete_article(file)
        fm.state_monitor.remove.assert_called_with(file)

