import shutil
import sys, getopt
import json
import os
from graphsitegen import filesystem
from graphsitegen import article
from graphsitegen import htmlutils
from graphsitegen import graph

class Builder:
	def __init__(self, input_folder, output_folder, templates_folder) -> None:
		self.input_folder = input_folder
		self.output_folder = output_folder
		self.templates_folder = templates_folder
		self.filemgr = filesystem.FileManager(self.input_folder, self.output_folder, self.templates_folder)
		self.reader = article.ArticleReader(self.filemgr)
		self.graph_generator = graph.GraphGenerator(self.reader)
		self.html_generator = htmlutils.HtmlGenerator(self.filemgr)
		self.linker = filesystem.FileLinker(self.filemgr, self.reader)

	# Parse python script arguments (input, output, template or settings file)
	def from_args(argv):
		try:
			opts, args = getopt.getopt(argv, "hi:o:t:f:", ["input=", "output=", "templates=", "file="])
		except getopt.GetoptError:
			print('script arguments: -i <inputFolder> -o <outputFolder> -t <templatesFolder>')
			sys.exit(2)

		input_folder = './articles'
		output_folder = './docs'
		templates_folder = './templates'

		for opt, arg in opts:
			if opt == "-h":
				print("Usage:")
				print("python generator.py -f <settingsFile>")
				print("or")
				print("python generator.py -i <inputFolder> -o <outputFolder> -t <templatesFolder>")
				sys.exit(1)
			elif opt in ("-i", "--input"):
				input_folder = arg
			elif opt in ("-o", "--output"):
				output_folder = arg
			elif opt in ("-t", "--templates"):
				templates_folder = arg
			elif opt in ("-f", "--file"):
				return Builder.from_settings(arg)

		return Builder(input_folder, output_folder, templates_folder)

	# Reads settings from a file
	# File should contain the following JSON content:
	# {
	#    'input': '/path/to/input/folder',
	#	 'output': '/path/to/output/folder',
	#	 'templates': '/path/to/templates/folder'	
	# }
	def from_settings(settings_file):
		with open(settings_file, 'r') as f:
			settings = json.loads(f.read())
		return Builder(settings['input'], settings['output'], settings['templates'])

	def run(self):
		print("Start generating files from " + str(self.input_folder) + " to " + str(self.output_folder))
		print("Templates are in " + str(self.templates_folder))

		changed_sources = self.filemgr.list_changed_source()
		if not any(changed_sources):
			print('Nothing changed.')
			exit()

		self.update_new_links()
		self.generate_sources(changed_sources)
		self.generate_fixed_pages()

	def update_new_links(self):
		self.linker.create_new_files()
		self.linker.update_missing_links()

	def generate_sources(self, changed_sources):
		print(str(len(changed_sources)) + " articles changed.")
		for file in changed_sources:
			if not self.filemgr.exists(file.name):
				self.filemgr.delete_article(file)
				continue
			article = self.reader.read_article(file.name)
			graph_svg = self.graph_generator.generate_article(article)
			self.html_generator.generate_article(article, graph_svg)

	def generate_fixed_pages(self):
		shutil.copyfile(os.path.join(self.filemgr.template_location, 'index.html'), self.filemgr.render_folder + "index.html")
		self.html_generator.generate_map(self.graph_generator.generate_full(self.filemgr.list_source()))
		self.generate_news()

	def generate_news(self):
		print("Generating news feed...")
		article_files = self.filemgr.list_source()
		articles = []
		for file in article_files:
			article = self.reader.read_article(file.name)
			articles.append(article)

		articles.sort(key=lambda x: x.publication_date, reverse=True)
		self.html_generator.generate_news(articles)

if __name__ == "__main__":
	Builder.from_args(sys.argv[1:]).run()
