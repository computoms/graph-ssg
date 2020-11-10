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
import filechanges


# Utils

def display(text):
	print(text)


# FileManager class handles the source files and their state. 
class FileManager:
	def __init__(self, source_folder):
		self.source_folder = source_folder
		self.changes = filechanges.FileChangeRegister("changes.txt")

	def get_files(self):
		raw_source_files = []
		for (dirpath, dirnames, filenames) in walk(self.source_folder):
			raw_source_files.extend(filenames)

		source_files = []
		for f in raw_source_files:
			if f != ".DS_Store":
				source_files.append(f)

		return source_files

	def get_changed_files(self):
		files = self.get_files()
		return [file for file in files if self.changes.has_changed(self.source_folder + file)]

	def sync(self, filename):
		self.changes.update(self.source_folder + filename)

# PageGenerator class handles the generation of html pages from markdown source files
class PageGenerator:
	def __init__(self, template_folder, template):
		self.template = template
		if template_folder[-1] == '/':
			template_folder = template_folder[:-1]
		self.template_location = template_folder

	def generate(self, data, output_filename): # TODO should contain output_folder in the path
		env = Environment(loader=PackageLoader('sitegenerator', self.template_location))
		page_template = env.get_template(self.template)
		content_html = page_template.render(post=data)

		with open(output_filename, "w") as file:
			display("  - Generating " + output_filename)
			file.write(content_html)

# Specialized class that uses a PageGenerator to generate articles
# from the 'page_template.html' template.
class ArticleGenerator:
	def __init__(self, template_folder, source_folder):
		self.generator = PageGenerator(template_folder, 'page_template.html')
		self.source_folder = source_folder

	def generate(self, json, md, output_filename):
		title = json["Title"]
		#abstract = json["Abstract"]

		data = {
		    'content': markdown.markdown(md),
		    'title': title,
		    'graph': graph.generate_graph(json, self.source_folder)
		}

		self.generator.generate(data, output_filename)

# The SourceLinker class handles the creation of new child source files
# as well as checks and updates the links between articles to keep them up-to-date.
class SourceLinker:
	def __init__(self, source_folder):
		self.source_folder = source_folder
		self.open_editor_on_create = True

	def create_empty_source_file(self, filename, parent, title, children = ''):
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

	def open_editor(self, filename):
		os.system('subl "' + filename + '"')

	def create_children(self, source_files):
		display("Creating new children...")
		new_files = []
		for f in source_files:
			json, markdown = article.parse(f, self.source_folder)
			for child in json["Children"]:
				if child == "":
					continue

				new_filename = self.source_folder + child + ".md"
				if not path.exists(self.source_folder + child + ".md"):
					self.create_empty_source_file(new_filename, json["Title"], child)
					new_files.append(new_filename)
					display("  - Created " + new_filename)
			if len(json['Parents']) == 0 or json['Parents'][0] == "":
				continue

			new_filename = self.source_folder + json["Parents"][0] + ".md"
			if not path.exists(new_filename):
				self.create_empty_source_file(new_filename, "", json["Parents"][0], json["Title"])
				new_files.append(new_filename)
				display("  - Created " + new_filename)

		for f in new_files:
			self.open_editor(f)


	def update_parents(self, source_files):
		display("Updating parent links...")
		for f in source_files:
			json, markdown = article.parse(f, self.source_folder)
			for child in json['Children']:
				if child == "":
					continue

				json_child, md_child = article.parse(child + ".md", self.source_folder)
				if not json['Title'] in json_child['Parents']:
					json_child['Parents'].append(json['Title'])
					article.save(json_child, md_child, self.source_folder + child + ".md")

# Main class to generate files for the site.
class SiteGenerator:

	def __init__(self):
		self.source_folder = "content/"
		self.output_folder = "output/"
		self.template_folder = "templates/"
		self.source_manager = FileManager(self.source_folder)
		self.article_generator = ArticleGenerator(self.template_folder, self.source_folder)
		self.source_linker = SourceLinker(self.source_folder)

	def generate_map(self):
		data = {
	    	'graph': graph.generate_full_graph(self.source_folder, self.source_manager.get_files()),
	    	'title': "Graph"
		}
		page_generator = PageGenerator(self.template_folder, 'map_template.html')
		page_generator.generate(data, self.output_folder + 'map.html')

	def generate_pages(self):
		display("Generating fixed pages...")
		shutil.copyfile('templates/index.html', self.output_folder + "index.html")
		self.generate_map()

	def generate_articles(self):
		files = self.source_manager.get_changed_files()
		if len(files) == 0:
			display("Source files did not change.")
		else:
			display(str(len(files)) + " files updated. Generating outputs...")
		for f in files:
			json, markdown = article.parse(f, self.source_folder)
			file_name = f[:-3] + ".html"
			self.article_generator.generate(json, markdown, self.output_folder + file_name)
			self.source_manager.sync(f)

	def update(self):
		source_files = self.source_manager.get_changed_files()
		self.source_linker.create_children(source_files)
		self.source_linker.update_parents(source_files)
		self.generate_pages()
		self.generate_articles()


if __name__ == "__main__":
    g = SiteGenerator()
    g.update()
