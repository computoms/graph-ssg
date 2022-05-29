from graphsitegen.articlereader import ArticleReader
from graphsitegen.filesystem.filemanager import FileManager
from graphsitegen.filesystem.filelinker import FileLinker
from graphsitegen.article import Article
from graphsitegen.article import ArticleFile

class FileManagerMockForLinks(FileManager):
    def __init__(self):
        self.articles = []
        self.source = {}
        self.output = ""

    def create_article_file(self, name):
        source = name + '.md'
        output = name + '.html'
        return ArticleFile(name, source, output)

    def list_source(self):
        return [self.create_article_file(article.title) for article in self.articles]

    def list_changed_source(self):
        return self.list_source(self)

    def exists(self, name):
        return name in [s.name for s in self.list_source()]

    def get_full_path(self, name):
        return name

    def get_article_internal(self, name):
        for article in self.articles:
            if article.title == name:
                return article

    def get_source_content(self, file):
        article = self.get_article_internal(file.name)
        a = ArticleReader(self)
        content = a.get_frontmatter_json(article) + "\n" + article.content
        return content

    def set_source_content(self, name, content):
        self.source[name] = content

    def save_output(self, name, content):
        self.output = content

class TestFileLinker:
    def setup_method(self, method):
        self.f = FileManagerMockForLinks()
        self.reader = ArticleReader(self.f)
        self.linker = FileLinker(self.f, self.reader)
        self.linker.open_editor_on_create = False
    
    def test_WithParentWithNoChildren_WhenUpdatingChildren_ThenUpdatesParentWithOneChild(self):
        self.f.articles.append(Article("Parent01", [], [], "2020-01-01", "", ""))
        self.f.articles.append(Article("Children01", ["Parent01"], [], "2020-01-01", "", ""))
        self.linker.update_children()
        assert "Children01" in self.f.source['Parent01']

    def test_WithChildrenWithoutParent_WhenUpdatingParent_ThenUpdatesChildrenWithOneParent(self):
        self.f.articles.append(Article("Parent01", [], ["Children01"], "", "", ""))
        self.f.articles.append(Article("Children01", [], [], "", "", ""))
        self.linker.update_parents()
        assert "Parent01" in self.f.source['Children01']

    def test_WithParentWithExistingChildren_WhenCreatingNewFile_ThenCreatesNewChildren(self):
        self.f.articles.append(Article("Parent01", [], ["Children01"], "", "", ""))
        self.linker.create_new_files()
        assert len(self.f.source) == 1
        assert self.f.source['Children01'] != ""

    def test_WithChildWithExistingParent_WhenCreatingNewFiles_ThenCreatesNewParent(self):
        self.f.articles.append(Article("Children01", ["Parent01"], [], "", "", ""))
        self.linker.create_new_files()
        assert len(self.f.source) == 1
        assert self.f.source['Parent01'] != ""