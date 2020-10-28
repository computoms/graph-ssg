from os import walk
from os import path
import os
import json as jsonlib
from graphviz import Digraph
import markdown
import getopt
import sys
from jinja2 import Environment, PackageLoader

import graph
import article

try:
	opts, args = getopt.getopt(sys.argv[1:], "ug", ["update", "generate"])
except getopt.GetoptError:
	print 'parse.py [-u] [-g]'
	sys.exit(2)

update = False
generate = False
for opt, arg in opts:
	if opt == '-u':
		update = True
	elif opt == '-g':
		generate == True

if (not update) and (not generate):
	update = True
	generate = True

def display(text):
	print(text)

# Static site generator that parses the files inside content/ subfolder and extracts information from their content (markdown files) + frontmatter in JSON
source_folder = "content/"
output_folder = "output/"

display("Parsing " + source_folder + " folder")

raw_source_files = []
for (dirpath, dirnames, filenames) in walk(source_folder):
	raw_source_files.extend(filenames)

source_files = []
for f in raw_source_files:
	if f != ".DS_Store":
		source_files.append(f)


def generate_html(json, md):
	title = json["Title"]
	abstract = json["Abstract"]

	env = Environment(loader=PackageLoader('sitegenerator', 'templates'))
	page_template = env.get_template('page_template.html')

	data = {
	    'content': markdown.markdown(md),
	    'title': title,
	    'graph': graph.generate_graph(json, source_folder)
	}

	return page_template.render(post=data)

def create_file(filename, parent, title, children = ''):
	output = "{\n"
	output += '    "Title": "' + title + '",\n'
	output += '    "Abstract": "",\n'
	output += '    "Parents": ["' + parent + '"],\n'
	output += '    "Children": ["' + children + '"]\n'
	output += '}\n'
	output += '\n'
	output += '# ' + title + '\n'

	with open(filename, "w") as file:
		file.write(output)


def create_new_files():
	display("Creating new source files for children / parents")

	new_files = []
	for f in source_files:
		json, markdown = article.parse(f, source_folder)
		for child in json["Children"]:
			if child == "":
				continue

			new_filename = source_folder + child + ".md"
			if not path.exists(source_folder + child + ".md"):
				create_file(new_filename, json["Title"], child)
				new_files.append(new_filename)
				display("  - Created " + new_filename)
		if len(json['Parents']) == 0 or json['Parents'][0] == "":
			continue

		new_filename = source_folder + json["Parents"][0] + ".md"
		if not path.exists(new_filename):
			create_file(new_filename, "", json["Parents"][0], json["Title"])
			new_files.append(new_filename)
			display("  - Created " + new_filename)

	return new_files

def check_parents():
	display("Updating parent linkings...")
	for f in source_files:
		json, markdown = article.parse(f, source_folder)
		for child in json['Children']:
			if child == "":
				continue

			json_child, md_child = article.parse(child + ".md", source_folder)
			if not json['Title'] in json_child['Parents']:
				json_child['Parents'].append(json['Title'])
				article.save(json_child, md_child, source_folder + child + ".md")

def generate_outputs():
	display("Generating output...")
	for f in source_files:
		json, markdown = article.parse(f, source_folder)
		generated_html = generate_html(json, markdown)
		file_name = output_folder + f[:-3] + ".html"
		with open(file_name, "w") as file:
			display("  - Generated " + file_name)
			file.write(generated_html)

def open_editor(filename):
	os.system('subl "' + filename + '"')

def generate_index():
	env = Environment(loader=PackageLoader('sitegenerator', 'templates'))
	page_template = env.get_template('page_template.html')

	data = {
	    'content': 'Welcome to Computoms website.',
	    'title': 'Computoms',
	    'graph': '<p>Generate Website graph'
	}

	content_html = page_template.render(post=data)
	with open(output_folder + "index.html", "w") as file:
		display("  - Generating index " + output_folder + "index.html")
		file.write(content_html)

def generate_fixed_page(title, content, graph, filename):
	env = Environment(loader=PackageLoader('sitegenerator', 'templates'))
	page_template = env.get_template('page_template.html')

	data = {
	    'content': content,
	    'title': title,
	    'graph': graph
	}

	content_html = page_template.render(post=data)
	with open(output_folder + filename, "w") as file:
		display("  - Generating " + output_folder + filename)
		file.write(content_html)

def generate_pages():
	generate_fixed_page('Blog', '', graph.generate_full_graph(source_folder, source_files), 'map.html')
	generate_fixed_page('Computoms', 'Welcome to Computoms website.', '', 'index.html')
	generate_fixed_page('About', 'About Computoms', '', 'about.html')
	generate_fixed_page('Contact', 'Contact information', '', 'contact.html')


# Script start
if update:
	new_files = create_new_files()
	for nf in new_files:
		open_editor(nf)

	check_parents()

if generate:
	generate_outputs()
	generate_pages()
	
