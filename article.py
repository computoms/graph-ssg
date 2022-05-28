import datetime

class Article:	

	def __init__(self, title, parents, children, publication_date, abstract, content):
		self.title = title
		self.parents = parents
		self.children = children
		self.content = content
		self.publication_date = publication_date
		self.abstract = abstract

	def get_publication_date_pretty(self):
		pub_date_obj = datetime.datetime.strptime(self.publication_date, "%Y-%m-%d")
		return pub_date_obj.strftime("%B %d, %Y")

class ArticleFile:
	def __init__(self, name, source, output) -> None:
		self.name = name
		self.source = source
		self.output = output
		self.is_template = False

