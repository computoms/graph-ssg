from graphsitegen.articlereader import ArticleReader
from graphsitegen.article import Article
from graphsitegen.filesystem.filemanager import FileManager
from graphsitegen import article

class FileManagerMock(FileManager):
	def __init__(self):
		self.source = ""
		self.output = ""

	def create_article_file(self, name):
		source = name + '.md'
		output = name + '.html'
		return article.ArticleFile(name, source, output)

	def apply_filter(self, source_file):
		for filt in self.file_filters:
			if filt in source_file:
				return False
		return True

	def list_source(self):
		return [self.create_article_file('Source01'), self.create_article_file('Source02'), self.create_article_file('Source03')]

	def list_changed_source(self):
		return ['Source02']

	def exists(self, name):
		return name in self.list_source()

	def get_full_path(self, name):
		return name

	def get_source_content(self, name):
		return '{"Title": "Test", "Abstract": "", "Children": ["Children01", "Children02"], "Parents": ["Parent01"], "Date": "2020-01-02"} Content'

	def set_source_content(self, name, content):
		self.source = content

	def save_output(self, name, content):
		self.output = content


class TestArticle:
	def test_WhenGettingPublicationDatePretty_ThenReturnsPrettyDate(self):
		a = Article('', '', '', '2020-05-01', '', '')
		assert a.get_publication_date_pretty() == "May 01, 2020"

class TestArticleReader:
	def setup_method(self, method):
		self.reader = ArticleReader(FileManagerMock())
		self.article = self.reader.read_article('Source01')

	def test_WithValidArtcile_WhenReadingArticle_ThenReturnsValidTitle(self):
		assert self.article.title == "Test"

	def test_WithValidArtcile_WhenReadingArticle_ThenReturnsValidParents(self):
		assert len(self.article.parents) == 1 
		assert self.article.parents[0] == "Parent01" 

	def test_WithValidArtcile_WhenReadingArticle_ThenReturnsValidChildren(self):
		assert len(self.article.children) == 2
		assert self.article.children[0] == "Children01"
		assert self.article.children[1] == "Children02"

	def test_WithValidArtcile_WhenReadingArticle_ThenReturnsValidContent(self):
		article = self.reader.read_article('Source01')
		assert article.content == " Content"

	def test_WithValidArticle_WhenSavingArticle_ThenSavesCorrectlyFormattedArticle(self):
		article = Article("TestArticle", ["Parent01"], ["Children01", "Children02"], "2020-01-01", "", "This is the article content.")
		self.reader.save_article(article)
		assert self.reader.filemgr.source == '{\n"Title": "TestArticle",\n"Abstract": "", \n"Parents": ["Parent01"], \n"Children": ["Children01","Children02"], \n"Date": "2020-01-01" \n}\nThis is the article content.'

