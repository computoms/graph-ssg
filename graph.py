import json
from graphviz import Digraph

import article

def is_valid(collection):
	return len(collection) != 0 and collection[0] != ""

def add_center_node(g, node_title):
	g.attr('node', color='gray')
	g.node(node_title)
	g.attr('node', color='green')

def add_node(g, node_title):
	if node_title == "":
		return
	g.node(node_title, href=node_title + ".html")

def add_children(g, node, linked_nodes):
	if node == "":
		return

	for n in linked_nodes:
		if n == "":
			continue
		g.node(n, href=n + ".html")
		g.edge(node, n)

def add_parent_level(g, parents, title, source_folder):
	if not is_valid(parents):
		add_center_node(g, title)
		return

	for parent in parents:
		if parent == "":
			continue
		add_node(g, parent)

		for parentChild in article.get_children(parent + '.md', source_folder):
			if parentChild == "":
				continue
			if parentChild == title:
				add_center_node(g, title)
			else:
				add_node(g, parentChild)
			g.edge(parent, parentChild)

def generate_graph(json, source_folder):
	title = json['Title']
	parents = json['Parents']
	children = json['Children']

	g = Digraph(name=title, node_attr={'color': 'green', 'style': 'filled', 'shape': 'box', 'fontcolor': 'white'}, edge_attr={'arrowhead': 'none', 'arrowtail': 'dot'})

 	# Parent level, with first children
	add_parent_level(g, parents, title, source_folder)	

	# Center node's children
	add_children(g, title, children)
	# Second level children
	for child in children:
		if child == "":
			continue
		add_children(g, child, article.get_children(child + ".md", source_folder))


	g.format='svg'
	return g.pipe().decode('utf-8')

def generate_full_graph(source_folder, source_files):
	g = Digraph(name='Full Map', node_attr={'color': 'green', 'style': 'filled', 'shape': 'box', 'fontcolor': 'white'}, edge_attr={'arrowhead': 'none', 'arrowtail': 'dot'})
	for f in source_files:
		json, markdown = article.parse(f, source_folder)
		g.node(json['Title'], href=json['Title'] + '.html')
	for f in source_files:
		json, markdown = article.parse(f, source_folder)
		for child in json['Children']:
			if child != "":
				g.edge(json['Title'], child)
	g.format='svg'
	return g.pipe().decode('utf-8')
