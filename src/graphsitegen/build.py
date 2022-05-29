from graphsitegen.filesystem import filechanges as fsc
from graphsitegen.filesystem import filemanager as fsm
from graphsitegen.filesystem import filelinker as fsl
from graphsitegen.articlereader import ArticleReader
from graphsitegen.article import Article
from graphsitegen import htmlutils
from graphsitegen import graph
import shutil
import sys, getopt
import json
import os


# Reads settings from a file
# File should contain the following JSON content:
# {
#    'input': '/path/to/input/folder',
#	 'output': '/path/to/output/folder',
#	 'templates': '/path/to/templates/folder'	
# }
def readSettingsFile(filename):
	with open(filename, "r") as file:
		settings = json.loads(file.read())

	return settings['input'], settings['output'], settings['templates'], filename

# Parse python script arguments (input, output, template or settings file)
def parseArguments(argv):
	inputFolder = ''
	outputFolder = ''
	templatesFolder = ''
	settingsFile = ''
	try:
		opts, args = getopt.getopt(argv, "hi:o:t:f:", ["input=", "output=", "templates=", "file="])
	except getopt.GetoptError:
		print('script arguments: -i <inputFolder> -o <outputFolder> -t <templatesFolder>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
			print("Usage:")
			print("python generator.py -f <settingsFile>")
			print("or")
			print("python generator.py -i <inputFolder> -o <outputFolder> -t <templatesFolder>")
			sys.exit(1)
		elif opt in ("-i", "--input"):
			inputFolder = arg
		elif opt in ("-o", "--output"):
			outputFolder = arg
		elif opt in ("-t", "--templates"):
			templatesFolder = arg
		elif opt in ("-f", "--file"):
			return readSettingsFile(arg)

	return inputFolder, outputFolder, templatesFolder, settingsFile

def main(argv):

	inputFolder, outputFolder, templatesFolder, settingsFile = parseArguments(argv)
	print("Start generating files from " + str(inputFolder) + " to " + str(outputFolder))
	print("Templates are in " + str(templatesFolder))

	filemgr = fsm.FileManager(inputFolder, outputFolder, templatesFolder)
	reader = ArticleReader(filemgr)
	graph_generator = graph.GraphGenerator(reader)
	html_generator = htmlutils.HtmlGenerator(filemgr)
	linker = fsl.FileLinker(filemgr, reader)

	def update_new_links():
		linker.create_new_files()
		linker.update_missing_links()

	def generate_sources(changed_sources):
		print(str(len(changed_sources)) + " articles changed.")
		for file in changed_sources:
			if not filemgr.exists(file.name):
				filemgr.delete_article(file)
				continue
			article = reader.read_article(file.name)
			graph_svg = graph_generator.generate_article(article)
			html_generator.generate_article(article, graph_svg)


	def generate_news():
		print("Generating news feed...")
		article_files = filemgr.list_source()
		articles = []
		for file in article_files:
			article = reader.read_article(file.name)
			articles.append(article)

		articles.sort(key=lambda x: x.publication_date, reverse=True)
		html_generator.generate_news(articles)

	def generate_fixed_pages():
		shutil.copyfile(os.path.join(filemgr.template_location, 'index.html'), filemgr.render_folder + "index.html")
		html_generator.generate_map(graph_generator.generate_full(filemgr.list_source()))
		generate_news()

	changed_sources = filemgr.list_changed_source()
	if not any(changed_sources):
		print('Nothing changed.')
		exit()

	update_new_links()
	generate_sources(changed_sources)
	generate_fixed_pages()


if __name__ == "__main__":
	main(sys.argv[1:])
