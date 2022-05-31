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

	def print_help_and_exit():
		print("Usage:")
		print("python generator.py -f <settingsFile>")
		print("or")
		print("python generator.py -i <inputFolder> -o <outputFolder> -t <templatesFolder>")
		sys.exit(1)

	# Parse python script arguments (input, output, template or settings file)
	def from_args(args):
		help_arg = ('-h', '--help', False)
		settings_file_arg = ('-f', '--file', True)
		input_arg = ('-i', '--input', True)
		output_arg = ('-o', '--output', True)
		templates_arg = ('-t', '--templates', True)
		known_args = [help_arg, settings_file_arg, input_arg, output_arg, templates_arg]

		options = Builder.parse_arguments(known_args, args)

		if options.has(help_arg):
			Builder.print_help_and_exit()
			
		if options.has(settings_file_arg):
			return Builder.from_settings(options.value(settings_file_arg).evaluate())

		input_folder = options.value(input_arg).with_default('./article')
		output_folder = options.value(output_arg).with_default('./docs')
		templates_folder = options.value(templates_arg).with_default('./templates')

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

	def parse_arguments(arguments, argv):
		shorts, longs = Builder.extract_settings(arguments)
		try:
			opts, args = getopt.getopt(argv, shorts, longs)
			return ProgramOptions(opts)
		except getopt.GetoptError:
			print('script arguments: -i <inputFolder> -o <outputFolder> -t <templatesFolder>')
			sys.exit(2)
			return ProgramOptions([])

	def extract_settings(arguments):
		short = ''.join([x[0][1] + (':' if x[2] else '') for x in arguments])
		long = [x[1][2:] + "=" for x in filter(lambda x: x[2], arguments)]
		return short, long

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
		shutil.copyfile(os.path.join(self.filemgr.template_location, 'index.html'), os.path.join(self.filemgr.render_folder, "index.html"))
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

class ProgramOptions:
	def __init__(self, options) -> None:
		self.options = options

	def value(self, argument):
		return Optional(map(lambda y: y[1], filter(lambda x: x[0] in (argument[0], argument[1]), self.options)))
	
	def has(self, argument):
		return any(filter(lambda x: x[0] in (argument[0], argument[1]), self.options))

class Optional:
	def __init__(self, iterable) -> None:
		self.iterable = iterable

	def with_default(self, default_value):
		l = list(self.iterable)
		return default_value if len(l) == 0 else l[0]

	def evaluate(self):
		return next(self.iterable)

if __name__ == "__main__":
	Builder.from_args(sys.argv[1:]).run()
