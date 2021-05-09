import model as modellib
import htmlutils
import graph
import shutil
import collections


filemgr = modellib.FileManager()
reader = modellib.ArticleReader(filemgr)
graph_generator = graph.GraphGenerator(reader)
html_generator = htmlutils.HtmlGenerator(filemgr)
linker = modellib.FileLinker(filemgr, reader)

def update_new_links():
	linker.create_new_files()
	linker.update_missing_links()

def generate_sources():
	article_names = filemgr.list_changed_source()
	print(str(len(article_names)) + " articles changed.")
	for name in article_names:
		article = reader.read_article(name)
		graph_svg = graph_generator.generate(article)
		html_generator.generate_article(article, graph_svg)

def generate_news():
	print("Generating news feed...")
	article_names = filemgr.list_source()
	articles = []
	for name in article_names:
		article = reader.read_article(name)
		articles.append(article)

	articles.sort(key=lambda x: x.publication_date, reverse=True)
	html_generator.generate_news(articles)


def generate_fixed_pages():
	shutil.copyfile('templates/index.html', filemgr.render_folder + "index.html")
	html_generator.generate_map(graph_generator.generate_full(filemgr.list_source()))
	generate_news()

if len(filemgr.list_changed_source()) == 0:
	print('Nothing changed.')
	exit()

update_new_links()
generate_sources()
generate_fixed_pages()
