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

class ArticleReaderTest:

	def readarticle_validarticle_returnsvalidtitle(self):
		f = TestingFileManager()
		a = model.ArticleReader(f)
		article = a.read_article('Source01')
		assert(article.title == "Test")

	def readarticle_validarticle_returnsvalidparents(self):
		f = TestingFileManager()
		a = model.ArticleReader(f)
		article = a.read_article('Source01')
		assert(len(article.parents) == 1)
		assert(article.parents[0] == "Parent01")


	def readarticle_validarticle_returnsvalidchildren(self):
		f = TestingFileManager()
		a = model.ArticleReader(f)
		article = a.read_article('Source01')
		assert(len(article.children) == 2)
		assert(article.children[0] == "Children01")
		assert(article.children[1] == "Children02")

	def readarticle_validarticle_returnsvalidcontent(self):
		f = TestingFileManager()
		a = model.ArticleReader(f)
		article = a.read_article('Source01')
		assert(article.content == " Content")

	def savearticle_savescorrectlyformattedarticle(self):
		f = TestingFileManager()
		a = model.ArticleReader(f)
		article = model.Article("TestArticle", ["Parent01"], ["Children01", "Children02"], "This is the article content.")
		a.save_article(article)
		assert(f.source == '{\n"Title": "TestArticle",\n"Abstract": "", \n"Parents": ["Parent01"], \n"Children": ["Children01","Children02"] \n}\nThis is the article content.')


class TestingFileManagerForLinks:
	def __init__(self):
		self.articles = []
		self.source = {}
		self.output = ""

	def apply_filter(self, source_file):
		for filt in self.file_filters:
			if filt in source_file:
				return False
		return True

	def list_source(self):
		return [article.title for article in self.articles]

	def list_changed_source(self):
		return list_source(self)

	def exists(self, name):
		return name in self.list_source()

	def get_full_path(self, name):
		return name

	def get_article_internal(self, name):
		for article in self.articles:
			if article.title == name:
				return article

	def get_source_content(self, name):
		article = self.get_article_internal(name)
		a = model.ArticleReader(self)
		content = a.get_frontmatter_json(article) + "\n" + article.content
		return content

	def set_source_content(self, name, content):
		self.source[name] = content

	def save_output(self, name, content):
		self.output = content

class FileLinkerTest:
	def updatechildren_parentwithnochildren_updatesparentwithonechildren(self):
		f = TestingFileManagerForLinks()
		f.articles.append(model.Article("Parent01", [], [], ""))
		f.articles.append(model.Article("Children01", ["Parent01"], [], ""))
		reader = model.ArticleReader(f)
		linker = model.FileLinker(f, reader)
		linker.update_children()
		assert("Children01" in f.source['Parent01'])

	def updateparent_childrenwithnoparent_updateschildrenwithoneparent(self):
		f = TestingFileManagerForLinks()
		f.articles.append(model.Article("Parent01", [], ["Children01"], ""))
		f.articles.append(model.Article("Children01", [], [], ""))
		reader = model.ArticleReader(f)
		linker = model.FileLinker(f, reader)
		linker.update_parents()
		assert("Parent01" in f.source['Children01'])

	def createnewfiles_parentwithinexistantchildren_createsnewchildren(self):
		f = TestingFileManagerForLinks()
		f.articles.append(model.Article("Parent01", [], ["Children01"], ""))
		reader = model.ArticleReader(f)
		linker = model.FileLinker(f, reader)
		linker.open_editor_on_create = False
		linker.create_new_files()
		assert(len(f.source) == 1)
		assert(f.source['Children01'] != "")

	def createnewfiles_childwithinexistingparent_createsnewparent(self):
		f = TestingFileManagerForLinks()
		f.articles.append(model.Article("Children01", ["Parent01"], [], ""))
		reader = model.ArticleReader(f)
		linker = model.FileLinker(f, reader)
		linker.open_editor_on_create = False
		linker.create_new_files()
		assert(len(f.source) == 1)
		assert(f.source['Parent01'] != "")


article_reader_test = ArticleReaderTest()
article_reader_test.readarticle_validarticle_returnsvalidtitle()
article_reader_test.readarticle_validarticle_returnsvalidparents()
article_reader_test.readarticle_validarticle_returnsvalidchildren()
article_reader_test.readarticle_validarticle_returnsvalidcontent()
article_reader_test.savearticle_savescorrectlyformattedarticle()

file_linker_test = FileLinkerTest()
file_linker_test.updatechildren_parentwithnochildren_updatesparentwithonechildren()
file_linker_test.updateparent_childrenwithnoparent_updateschildrenwithoneparent()
file_linker_test.createnewfiles_parentwithinexistantchildren_createsnewchildren()
file_linker_test.createnewfiles_childwithinexistingparent_createsnewparent()