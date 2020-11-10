import json as jsonlib
from os import walk
from os import path
import graph
import filechanges

class Model:
	def __init__(self):
		self.source_folder = "content/"
		self.source_extension = ".md"
		self.template_location = "templates/"
		self.render_folder = "output/"
		self.render_extension = ".html"
		self.template_name = "page_template.html"
		self.change_register = filechanges.FileChangeRegister("changes.txt")
		self.file_filters = [".DS_Store"]
		# TODO Add file filters (like .DS_Store)

	def get_source_content(self, name):
		if not path.exists(self.source_folder + name + self.source_extension):
			return ['']
		with open(self.source_folder + name + self.source_extension, "r") as file:
			return file.readlines()

	def save(self, name, content):
		with open(self.source_folder + name + self.source_extension, "w") as file:
			file.write(content)

	def save_render(self, name, content):
		with open(self.render_folder + name + self.render_extension, "w") as file:
			file.write(content)
		self.change_register.update(self.source_folder + name + self.source_extension)

	def is_valid(self, file, only_changed):
		for filt in self.file_filters:
			if filt in file:
				print(file + ' contains ' + filt)
				return False
		if not only_changed:
			return True
		return self.change_register.has_changed(file)

	def get_articles(self, only_changed = True):
		raw_source_files = []
		for (dirpath, dirnames, filenames) in walk(self.source_folder):
			raw_source_files.extend(filenames)

		source_files = []
		for f in raw_source_files:
			if self.is_valid(self.source_folder + f, only_changed):
				source_files.append(f[:-len(self.source_extension)])

		return [parse(self, name) for name in source_files]


class Article:	

	def __init__(self, title, parents, children, content):
		self.title = title
		self.parents = parents
		self.children = children
		self.content = content

	def save(article, model):
		content = Article.get_frontmatter_json(article) + "\n" + article.content
		model.save(self.name, content)

	@staticmethod
	def parse(model, name):
		source_markdown = ""
		source_json = ""

		source_lines = model.get_source_content(name)
		if len(source_lines) == 0:
			return Article("None", [], [], "")

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
		return Article(json['Title'], json['Parents'], json['Children'], source_markdown)

	@staticmethod
	def get_frontmatter_json(article):
		s = '","'
		return jsonlib.loads(\
			'{"Title": "' + article.title + '", \
			"Abstract": "", \
			"Parents": ["' + s.join([p for p in article.parents]) + '"], \
			"Children": ["' + s.join([c for c in article.children]) + '"]}')

	
	@staticmethod
	def get_graph_svg(article, model):
		return graph.generate_graph(Article.get_frontmatter_json(article), model.source_folder)
