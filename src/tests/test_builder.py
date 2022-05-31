import shutil
import sys
import unittest
from unittest.mock import MagicMock
from graphsitegen.article import Article, ArticleFile
from graphsitegen.build import Builder

class TestBuilder:
    def setup_method(self, method):
        self.builder = Builder('input', 'output', 'templates')
        self.count = 0

    def assert_article_order(self, articles):
        assert len(articles) == 2
        assert articles[0].title == 'article2'
        assert articles[1].title == 'article1'

    def test_WithTwoArticles_WhenGenerateNews_ThenGenerateNewsInPublicationOrder(self):
        self.builder.filemgr.list_source = MagicMock(return_value=[ArticleFile('article1', 'article1.md', 'article1.html'), ArticleFile('article2', 'article2.md', 'article2.html')])
        articles = [Article('article1', [], [], '2020-01-01', '', ''), Article('article2', [], [], '2020-01-02', '', '')]
        self.builder.reader.read_article = MagicMock(side_effect=articles)
        self.builder.html_generator.generate_news = MagicMock(side_effect=self.assert_article_order)
        self.builder.generate_news()

    def test_WhenGenerateFixedPages_ThenCopiesIndex(self):
        shutil.copyfile = MagicMock()
        self.builder.html_generator.generate_map = MagicMock()
        self.builder.html_generator.generate_news = MagicMock()
        self.builder.graph_generator.generate_full = MagicMock()
        self.builder.generate_fixed_pages()
        shutil.copyfile.assert_called_with('templates/index.html', 'output/index.html')
        
    def test_WhenGenerateFixedPages_ThenGeneratesMap(self):
        shutil.copyfile = MagicMock()
        self.builder.html_generator.generate_map = MagicMock()
        self.builder.html_generator.generate_news = MagicMock()
        self.builder.graph_generator.generate_full = MagicMock()
        self.builder.generate_fixed_pages()
        self.builder.graph_generator.generate_full.assert_called()
        self.builder.html_generator.generate_map.assert_called()

    def test_WhenGenerateFixedPages_ThenGeneratesNews(self):
        shutil.copyfile = MagicMock()
        self.builder.html_generator.generate_map = MagicMock()
        self.builder.html_generator.generate_news = MagicMock()
        self.builder.graph_generator.generate_full = MagicMock()
        self.builder.generate_fixed_pages()
        self.builder.html_generator.generate_news.assert_called()

    def test_WhenGenerateSources_ThenGenerateArticle(self):
        self.builder.filemgr.exists = MagicMock(return_value=True)
        article = Article('title', [], [], '2020-01-01', '', '')
        self.builder.reader.read_article = MagicMock(return_value=article)
        self.builder.graph_generator.generate_article = MagicMock()
        self.builder.html_generator.generate_article = MagicMock()
        self.builder.generate_sources([ArticleFile('title', '', '')])
        self.builder.graph_generator.generate_article.assert_called_with(article)
        self.builder.html_generator.generate_article.assert_called_with(article, unittest.mock.ANY)

    def test_WhenUpdateNewLinks_ThenCallsLinker(self):
        self.builder.linker.create_new_files = MagicMock()
        self.builder.linker.update_missing_links = MagicMock()
        self.builder.update_new_links()
        self.builder.linker.create_new_files.assert_called()
        self.builder.linker.update_missing_links.assert_called()

    def test_WhenRun_ThenUpdateNewLinksAndGenerateSourcesAndFixedPages(self):
        self.builder.update_new_links = MagicMock()
        self.builder.generate_sources = MagicMock()
        self.builder.generate_fixed_pages = MagicMock()
        self.builder.filemgr.list_changed_source = MagicMock(return_value=[ArticleFile('test', '', '')])
        self.builder.run()
        self.builder.update_new_links.assert_called()
        self.builder.generate_sources.assert_called()
        self.builder.generate_fixed_pages.assert_called()

    def test_WithShortArgs_WhenParseFromArgs_ThenParsesCorreclty(self):
        builder = Builder.from_args(['-i', 'input', '-o', 'output', '-t', 'template'])
        assert builder.input_folder == 'input'
        assert builder.output_folder == 'output'
        assert builder.templates_folder == 'template'
        

    def test_WithLongArgs_WhenParseFromArgs_ThenParsesCorreclty(self):
        builder = Builder.from_args(['--input', 'input', '--output', 'output', '--template', 'template'])
        assert builder.input_folder == 'input'
        assert builder.output_folder == 'output'
        assert builder.templates_folder == 'template'
        
    def test_WithFile_WhenParseFromArgs_ThenParsesCorreclty(self):
        Builder.from_settings = MagicMock()
        Builder.from_args(['-f', 'settings.json'])
        Builder.from_settings.assert_called_with('settings.json')

    def test_WithHelp_WhenParseFromArgs_ThenExists(self):
        sys.exit = MagicMock()
        Builder.from_args(['-h'])
        sys.exit.assert_called_with(1)

    def test_WithInvalidArguments_WhenParseFromArgs_ThenExits(self):
        sys.exit = MagicMock()
        Builder.from_args(['-i', 'input', '--invalid', 'nothing'])
        sys.exit.assert_called_with(2)

    def test_WhenExtractSettings_ThenReturnsCorrectGetOptsConfiguration(self):
        short, long = Builder.extract_settings([('-h', '--help', False), ('-f', '--file', True), ('-i', '--input', True)])
        assert short == 'hf:i:'
        assert long == ['file=', 'input=']