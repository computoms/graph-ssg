import model
import markdown
from jinja2 import Environment, PackageLoader

class HtmlGenerator:
	def __init__(self, model):
		self.model = model

	def generate_article(self, article):
		title = article.title
		data = {
		    'content': markdown.markdown(article.content),
		    'title': article.title,
		    'graph': model.Article.get_graph_svg(article, self.model)
		}	

		env = Environment(loader=PackageLoader('htmlutils', self.model.template_location))
		page_template = env.get_template(self.model.template_name)
		content_html = page_template.render(post=data)

		self.model.save_render(article.title, content_html)
		print("- Generated " + article.title)
