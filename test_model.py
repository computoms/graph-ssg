import model

class TestingFileManager:
	def __init__(self):
		self.source = ""
		self.output = ""

	def apply_filter(self, source_file):
		for filt in self.file_filters:
			if filt in source_file:
				return False
		return True

	def list_source(self):
		return ['Source01', 'Source02', 'Source03']

	def list_changed_source(self):
		return ['Source02']

	def exists(self, name):
		return name in self.list_source()

	def get_full_path(self, name):
		return name

	def get_source_content(self, name):
		return '{"Title": "Test", "Abstract": "", "Children": ["Children01", "Children02"], "Parents": ["Parent01"]} Content'

	def set_source_content(self, name, content):
		self.source = content

	def save_output(self, name, content):
		self.output = content

def articlereader_readarticle_validarticle_returnsvalidtitle():
	f = TestingFileManager()
	a = model.ArticleReader(f)
	article = a.read_article('Source01')
	assert(article.title == "Test")

def articlereader_readarticle_validarticle_returnsvalidparents():
	f = TestingFileManager()
	a = model.ArticleReader(f)
	article = a.read_article('Source01')
	assert(len(article.parents) == 1)
	assert(article.parents[0] == "Parent01")


def articlereader_readarticle_validarticle_returnsvalidchildren():
	f = TestingFileManager()
	a = model.ArticleReader(f)
	article = a.read_article('Source01')
	assert(len(article.children) == 2)
	assert(article.children[0] == "Children01")
	assert(article.children[1] == "Children02")

def articlereader_readarticle_validarticle_returnsvalidcontent():
	f = TestingFileManager()
	a = model.ArticleReader(f)
	article = a.read_article('Source01')
	assert(article.content == " Content")

def articlereader_savearticle_savescorrectlyformattedarticle():
	f = TestingFileManager()
	a = model.ArticleReader(f)
	article = model.Article("TestArticle", ["Parent01"], ["Children01", "Children02"], "This is the article content.")
	a.save_article(article)
	assert(f.source == '{\n"Title": "TestArticle",\n"Abstract": "", \n"Parents": ["Parent01"], \n"Children": ["Children01","Children02"] \n}\nThis is the article content.')



articlereader_readarticle_validarticle_returnsvalidtitle()
articlereader_readarticle_validarticle_returnsvalidparents()
articlereader_readarticle_validarticle_returnsvalidchildren()
articlereader_readarticle_validarticle_returnsvalidcontent()
articlereader_savearticle_savescorrectlyformattedarticle()