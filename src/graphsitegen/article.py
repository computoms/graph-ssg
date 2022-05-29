import datetime
import json as jsonlib

class ArticleReader:
	def __init__(self, filemgr):
		self.filemgr = filemgr

	def read_article(self, name):
		source_markdown = ""
		source_json = ""

		source_lines = self.filemgr.get_source_content(self.filemgr.create_article_file(name))
		if len(source_lines) == 0:
			return Article("None", [], [], "", "", "")

		is_font_matter = False
		open_count = 0
		close_count = 0
		for line in source_lines:
			for c in line:
				if c == '{':
					open_count = open_count + 1
					if is_font_matter == False and open_count == 1:
						is_font_matter = True

				if c == '}':
					open_count = open_count - 1

				if is_font_matter:
					source_json = source_json + c
				else:
					source_markdown = source_markdown + c

				if is_font_matter and open_count == 0:
					is_font_matter = False

		json = jsonlib.loads(source_json)
		return Article(json['Title'], json['Parents'], json['Children'], json['Date'], json['Abstract'], source_markdown)

	def get_frontmatter_json(self, article):
		s = '","'
		return '{\n' \
		+ '"Title": "' + article.title + '",\n' \
		+ '"Abstract": "' + article.abstract + '", \n' \
		+ '"Parents": ["' + s.join([p for p in article.parents]) + '"], \n' \
		+ '"Children": ["' + s.join([c for c in article.children]) + '"], \n' \
		+ '"Date": "' + article.publication_date + '" \n' \
		+ '}'

	def save_article(self, article):
		content = self.get_frontmatter_json(article) + "\n" + article.content
		self.filemgr.set_source_content(article.title, content)


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

