import json
from graphviz import Digraph

import model


class GraphGenerator:

	def __init__(self, article_reader):
		self.article_reader = article_reader


	def generate_full(self, articles):
		g = Digraph(name='Full Map', \
			node_attr={'color': 'green', 'style': 'filled', 'shape': 'box', 'fontcolor': 'white'}, \
			edge_attr={'arrowhead': 'none', 'arrowtail': 'dot'})
		for title in articles:
			g.node(title, href=title + '.html')
		for title in articles:
			article = self.article_reader.read_article(title)
			for child_title in article.children:
				if child_title != "":
					g.edge(title, child_title)
		g.format = 'svg'
		return g.pipe().decode('utf-8')

	def generate(self, article):
		g = Digraph(name=article.title, \
			node_attr={'color': 'green', 'style': 'filled', 'shape': 'box', 'fontcolor': 'white'}, \
			edge_attr={'arrowhead': 'none', 'arrowtail': 'dot'})

	 	# Parent level, with first children
		self.add_parent_level(g, article.parents, article.title)	

		# Center node's children
		self.add_children(g, article.title, article.children)
		# Second level children
		for child in article.children:
			if child == "":
				continue
			child_article = self.article_reader.read_article(child)
			self.add_children(g, child, child_article.children)

		g.format='svg'
		return g.pipe().decode('utf-8')


	def add_parent_level(self, g, parents, title):
		if not self.is_valid(parents):
			self.add_center_node(g, title)
			return

		for parent in parents:
			if parent == "":
				continue
			self.add_node(g, parent)

			parent_article = self.article_reader.read_article(parent)

			for parentChild in parent_article.children:
				if parentChild == "":
					continue
				if parentChild == title:
					self.add_center_node(g, title)
				else:
					self.add_node(g, parentChild)
				g.edge(parent, parentChild)


	def add_children(self, g, node, linked_nodes):
		if node == "":
			return

		for n in linked_nodes:
			if n == "":
				continue
			g.node(n, href=n + ".html")
			g.edge(node, n)


	def add_center_node(self, g, node_title):
		g.attr('node', color='gray')
		g.node(node_title)
		g.attr('node', color='green')

	def add_node(self, g, node_title):
		if node_title == "":
			return
		g.node(node_title, href=node_title + ".html")

	def is_valid(self, collection):
		return len(collection) != 0 and collection[0] != ""

	
	
	