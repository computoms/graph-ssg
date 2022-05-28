from article import ArticleFile
import markdown
from jinja2 import Environment, FileSystemLoader
import os

class HtmlGenerator:
	def __init__(self, filemgr):
		self.filemgr = filemgr

		
	def get_template(self, template_name):
		env = Environment(loader=FileSystemLoader(self.filemgr.template_location))
		return env.get_template(template_name)


	def generate_article(self, article, graph_svg):
		title = article.title
		data = {
		    'content': markdown.markdown(article.content),
		    'title': article.title,
		    'graph': graph_svg,
		    'publication_date': article.get_publication_date_pretty(),
		    'abstract': article.abstract
		}	

		page_template = self.get_template(self.filemgr.template_name)
		content_html = page_template.render(post=data)
		file = self.filemgr.create_article_file(article.title)
		self.filemgr.save_output(file, content_html)
		print("- Generated " + article.title)

	def generate_map(self, graph_svg):
		data = {
	    	'graph': graph_svg,
	    	'title': "Graph"
		}

		page_template = self.get_template(self.filemgr.template_map)
		content_html = page_template.render(post=data)
		self.filemgr.save_output(self.filemgr.create_template_file('map', self.filemgr.template_map), content_html)

	def generate_news(self, ordered_articles):
		data = ordered_articles

		page_template = self.get_template(self.filemgr.template_news)
		content_html = page_template.render(articles=data)
		self.filemgr.save_output(self.filemgr.create_template_file('news', self.filemgr.template_news), content_html)

