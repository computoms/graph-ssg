import model

class FileManagerMock:
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
		return '{"Title": "Test", "Abstract": "", "Children": ["Children01", "Children02"], "Parents": ["Parent01"], "Date": "2020-01-02"} Content'

	def set_source_content(self, name, content):
		self.source = content

	def save_output(self, name, content):
		self.output = content

class FileManagerMockForLinks:
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
		return self.list_source(self)

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

class TestArticle:
	def test_WhenGettingPublicationDatePretty_ThenReturnsPrettyDate(self):
		a = model.Article('', '', '', '2020-05-01', '', '')
		assert a.get_publication_date_pretty() == "May 01, 2020"

class TestArticleReader:

	def test_WithValidArtcile_WhenReadingArticle_ThenReturnsValidTitle(self):
		f = FileManagerMock()
		a = model.ArticleReader(f)
		article = a.read_article('Source01')
		assert article.title == "Test"

	def test_WithValidArtcile_WhenReadingArticle_ThenReturnsValidParents(self):
		f = FileManagerMock()
		a = model.ArticleReader(f)
		article = a.read_article('Source01')
		assert len(article.parents) == 1 
		assert article.parents[0] == "Parent01" 

	def test_WithValidArtcile_WhenReadingArticle_ThenReturnsValidChildren(self):
		f = FileManagerMock()
		a = model.ArticleReader(f)
		article = a.read_article('Source01')
		assert len(article.children) == 2
		assert article.children[0] == "Children01"
		assert article.children[1] == "Children02"

	def test_WithValidArtcile_WhenReadingArticle_ThenReturnsValidContent(self):
		f = FileManagerMock()
		a = model.ArticleReader(f)
		article = a.read_article('Source01')
		assert article.content == " Content"

	def test_WithValidArticle_WhenSavingArticle_ThenSavesCorrectlyFormattedArticle(self):
		f = FileManagerMock()
		a = model.ArticleReader(f)
		article = model.Article("TestArticle", ["Parent01"], ["Children01", "Children02"], "2020-01-01", "", "This is the article content.")
		a.save_article(article)
		assert f.source == '{\n"Title": "TestArticle",\n"Abstract": "", \n"Parents": ["Parent01"], \n"Children": ["Children01","Children02"], \n"Date": "2020-01-01" \n}\nThis is the article content.'

class TestFileLinker:
	def test_WithParentWithNoChildren_WhenUpdatingChildren_ThenUpdatesParentWithOneChild(self):
		f = FileManagerMockForLinks()
		f.articles.append(model.Article("Parent01", [], [], "2020-01-01", "", ""))
		f.articles.append(model.Article("Children01", ["Parent01"], [], "2020-01-01", "", ""))
		reader = model.ArticleReader(f)
		linker = model.FileLinker(f, reader)
		linker.update_children()
		assert "Children01" in f.source['Parent01']

	def test_WithChildrenWithoutParent_WhenUpdatingParent_ThenUpdatesChildrenWithOneParent(self):
		f = FileManagerMockForLinks()
		f.articles.append(model.Article("Parent01", [], ["Children01"], "", "", ""))
		f.articles.append(model.Article("Children01", [], [], "", "", ""))
		reader = model.ArticleReader(f)
		linker = model.FileLinker(f, reader)
		linker.update_parents()
		assert "Parent01" in f.source['Children01']

	def test_WithParentWithExistingChildren_WhenCreatingNewFile_ThenCreatesNewChildren(self):
		f = FileManagerMockForLinks()
		f.articles.append(model.Article("Parent01", [], ["Children01"], "", "", ""))
		reader = model.ArticleReader(f)
		linker = model.FileLinker(f, reader)
		linker.open_editor_on_create = False
		linker.create_new_files()
		assert len(f.source) == 1
		assert f.source['Children01'] != ""

	def test_WithChildWithExistingParent_WhenCreatingNewFiles_ThenCreatesNewParent(self):
		f = FileManagerMockForLinks()
		f.articles.append(model.Article("Children01", ["Parent01"], [], "", "", ""))
		reader = model.ArticleReader(f)
		linker = model.FileLinker(f, reader)
		linker.open_editor_on_create = False
		linker.create_new_files()
		assert len(f.source) == 1
		assert f.source['Parent01'] != ""