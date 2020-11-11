import model
import markdown
from jinja2 import Environment, PackageLoader

class HtmlGenerator:
	def __init__(self, filemgr):
		self.filemgr = filemgr

	def generate_article(self, article, graph_svg):
		title = article.title
		data = {
		    'content': markdown.markdown(article.content),
		    'title': article.title,
		    'graph': graph_svg
		}	

		env = Environment(loader=PackageLoader('htmlutils', self.filemgr.template_location))
		page_template = env.get_template(self.filemgr.template_name)
		content_html = page_template.render(post=data)

		self.filemgr.save_output(article.title, content_html)
		print("- Generated " + article.title)
