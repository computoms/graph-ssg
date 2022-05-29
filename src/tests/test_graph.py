from unittest.mock import MagicMock
from graphsitegen.graph import GraphGenerator
from graphsitegen.articlereader import ArticleReader
from graphsitegen.article import Article, ArticleFile
from graphsitegen.filesystem import filemanager
from graphviz import Digraph

class TestGraphGenerator:
    def setup_method(self, method):
        self.reader = MagicMock()
        self.generator = GraphGenerator(self.reader)
        self.g = Digraph()

    def get_digraph_source(self, lines):
        return 'digraph {' + ''.join([str('\n\t') + str(l) for l in lines]) + '\n}\n'

    def get_digraph_source_with_title(self, title, lines):
        return 'digraph ' + title + ' {' + ''.join([str('\n\t') + str(l) for l in lines]) + '\n}\n'

    def test_WithEmptyCollection_WhenIsValid_ThenReturnsFalse(self):
        assert self.generator.is_valid([]) == False

    def test_WithOneEmptyStringElement_WhenIsValid_ThenReturnsFalse(self):
        assert self.generator.is_valid(['']) == False

    def test_WithValidNode_WhenAddNode_ThenAddsNodeToDiagraph(self):
        self.generator.add_node(self.g, 'title')
        assert self.g.source == self.get_digraph_source(['title [href="title.html"]'])

    def test_WithInvalidNode_WhenAddNode_ThenDoesNotAddNode(self):
        self.generator.add_node(self.g, '')
        assert self.g.source == self.get_digraph_source([])

    def test_WhenAddCenterNode_ThenAddsCenterAttributes(self):
        self.generator.add_center_node(self.g, 'test')
        assert self.g.source == self.get_digraph_source(['node [color=gray]', 'test', 'node [color=green]'])

    def test_WithInvalidNode_WhenAddChildren_ThenDoesNotAdd(self):
        self.generator.add_children(self.g, '', ['test'])
        assert self.g.source == self.get_digraph_source([])

    def test_WithValidNode_WithOneChildren_WhenAddChildren_ThenAddsChildrenWithEdge(self):
        self.generator.add_children(self.g, 'node', ['child'])
        assert self.g.source == self.get_digraph_source(['child [href="child.html"]', '"node" -> child'])

    def test_WithValidNode_WithInvalidChildAndValidChild_WhenAddChildren_ThenDoesNotAddLinkToInvalidChild(self):
        self.generator.add_children(self.g, 'node', ['', 'child1'])
        assert self.g.source == self.get_digraph_source(['child1 [href="child1.html"]', '"node" -> child1'])

    def test_WithInvalidParent_WhenAddParentLevel_ThenAddsCenterNode(self):
        self.generator.add_center_node = MagicMock()
        self.generator.add_parent_level(self.g, [''], 'title')
        self.generator.add_center_node.assert_called_with(self.g, 'title')

    def test_WithOneParent_WhenAddParentLevel_ThenAddsParentLevelWithCurrentArticleCentered(self):
        self.reader.read_article = MagicMock(return_value=Article('parent_title', [], ['title'], '2020-01-01', '', ''))
        self.generator.add_parent_level(self.g, ['parent'], 'title')
        assert self.g.source == self.get_digraph_source(['parent [href="parent.html"]', 'node [color=gray]', 'title', 'node [color=green]', 'parent -> title'])

    def test_WithOneParentWithMultipleChildren_WhenAddParentLevel_ThenAddsParentLevelWithCurrentArticleCentered(self):
        self.reader.read_article = MagicMock(return_value=Article('parent_title', [], ['title', 'child2'], '2020-01-01', '', ''))
        self.generator.add_parent_level(self.g, ['parent'], 'title')
        assert self.g.source == self.get_digraph_source(['parent [href="parent.html"]', 'node [color=gray]', 'title', 'node [color=green]', 'parent -> title', 'child2 [href="child2.html"]', 'parent -> child2'])

    def test_WithOneParentWithOneInvalidChild_WhenAddParentLevel_ThenAddsParentLevelWithCurrentArticleCentered(self):
        self.reader.read_article = MagicMock(return_value=Article('parent_title', [], ['title', ''], '2020-01-01', '', ''))
        self.generator.add_parent_level(self.g, ['parent'], 'title')
        assert self.g.source == self.get_digraph_source(['parent [href="parent.html"]', 'node [color=gray]', 'title', 'node [color=green]', 'parent -> title'])

    def test_WithOneInvalidParent_WhenAddParentLevel_ThenSkipsInvalidParent(self):
        self.reader.read_article = MagicMock(return_value=Article('parent_title', [], ['title', ''], '2020-01-01', '', ''))
        self.generator.add_parent_level(self.g, ['parent', ''], 'title')
        assert self.g.source == self.get_digraph_source(['parent [href="parent.html"]', 'node [color=gray]', 'title', 'node [color=green]', 'parent -> title'])

    def test_WithLonelyArticle_WhenGenerate_ThenGeneratesSingleNodeGraph(self):
        g = self.generator.generate_internal(Article('title', [], [], '2020-01-01', '', ''))
        assert g.source == self.get_digraph_source_with_title('title', ['node [color=green fontcolor=white shape=box style=filled]', 'edge [arrowhead=none arrowtail=dot]', 'node [color=gray]', 'title', 'node [color=green]'])

    def test_WithOneChild_WhenGenerate_ThenGeneratesTwoNodesGraph(self):
        self.reader.read_article = MagicMock(return_value=Article('child', ['title'], [], '2020-01-01', '', ''))
        g = self.generator.generate_internal(Article('title', [], ['child'], '2020-01-01', '', ''))
        assert g.source == self.get_digraph_source_with_title('title', ['node [color=green fontcolor=white shape=box style=filled]', 'edge [arrowhead=none arrowtail=dot]', 'node [color=gray]', 'title', 'node [color=green]', 'child [href="child.html"]', 'title -> child'])
    
    def test_WithOneChildWithEmptyChild_WhenGenerate_ThenGeneratesTwoNodesGraph(self):
        self.reader.read_article = MagicMock(return_value=Article('child', ['title'], [], '2020-01-01', '', ''))
        g = self.generator.generate_internal(Article('title', [], ['child', ''], '2020-01-01', '', ''))
        assert g.source == self.get_digraph_source_with_title('title', ['node [color=green fontcolor=white shape=box style=filled]', 'edge [arrowhead=none arrowtail=dot]', 'node [color=gray]', 'title', 'node [color=green]', 'child [href="child.html"]', 'title -> child'])

    def test_WithOneArticle_WhenGenerateFull_ThenGeneratesOneArticleFullMap(self):
        self.reader.read_article = MagicMock()
        g = self.generator.generate_full_internal([ArticleFile('title', 'title.md', 'title.html')])
        assert g.source == self.get_digraph_source_with_title('"Full Map"', ['node [color=green fontcolor=white shape=box style=filled]', 'edge [arrowhead=none arrowtail=dot]', 'title [href="title.html"]'])
    
    def test_WithOneParentAndOneChild_WhenGenerateFull_ThenGeneratesTwoArticleFullMap(self):
        self.reader.read_article = MagicMock(return_value=Article('parent', [], ['child'], '2020-01-01', '', ''))
        g = self.generator.generate_full_internal([ArticleFile('parent', 'parent.md', 'parent.html')])
        assert g.source == self.get_digraph_source_with_title('"Full Map"', ['node [color=green fontcolor=white shape=box style=filled]', 'edge [arrowhead=none arrowtail=dot]', 'parent [href="parent.html"]', 'parent -> child'])
