from os import walk
from os import path
import os
import json as jsonlib
from graphviz import Digraph
import markdown
import getopt
import sys
from jinja2 import Environment, PackageLoader
import shutil

import graph
import article


# This scripts reads the 'content/' directory (containing source files
# as markdown) and generates corresponding output html files.

try:
	opts, args = getopt.getopt(sys.argv[1:], "ug", ["update", "generate"])
except getopt.GetoptError:
	print 'sitegenerator.py [-u] [-g]'
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

def generate_page_from_template(template, data, output_filename):
	env = Environment(loader=PackageLoader('sitegenerator', 'templates'))
	page_template = env.get_template(template)
	content_html = page_template.render(post=data)

	with open(output_folder + output_filename, "w") as file:
		display("  - Generating " + output_folder + output_filename)
		file.write(content_html)


def generate_content_page(json, md, output_filename):
	title = json["Title"]
	#abstract = json["Abstract"]

	data = {
	    'content': markdown.markdown(md),
	    'title': title,
	    'graph': graph.generate_graph(json, source_folder)
	}

	generate_page_from_template('page_template.html', data, output_filename)

def generate_fixed_page(json, content, filename):
	data = {
	    'content': markdown.markdown(content),
	    'title': json['Title']
	}

	generate_page_from_template('fixed_page_template.html', data, filename)

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
		file_name = f[:-3] + ".html"
		generate_content_page(json, markdown, file_name)

def open_editor(filename):
	os.system('subl "' + filename + '"')

def generate_fixed_page_from_markdown(markdown_filename, output_filename):
	json, content = article.parse(markdown_filename, 'pages/')
	generate_fixed_page(json, content, output_filename)

def generate_map():
	data = {
	    'graph': graph.generate_full_graph(source_folder, source_files),
	    'title': "Graph"
	}
	generate_page_from_template('map_template.html', data, 'map.html')

def generate_pages():
	shutil.copyfile('templates/index.html', output_folder + "index.html")
	generate_map()


# Script start
if update:
	new_files = create_new_files()
	for nf in new_files:
		open_editor(nf)

	check_parents()

if generate:
	generate_outputs()
	generate_pages()
	
