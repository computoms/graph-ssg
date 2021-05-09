import json as jsonlib
from os import walk
from os import path
import graph
import filechanges
import datetime


def display(text):
	print(text)


class Article:	

	def __init__(self, title, parents, children, publication_date, content):
		self.title = title
		self.parents = parents
		self.children = children
		self.content = content
		self.publication_date = publication_date

	def get_publication_date_pretty(self):
		pub_date_obj = datetime.datetime.strptime(self.publication_date, "%Y-%m-%d")
		return pub_date_obj.strftime("%B %d, %Y")

class ArticleReader:
	def __init__(self, filemgr):
		self.filemgr = filemgr

	def read_article(self, name):
		source_markdown = ""
		source_json = ""

		source_lines = self.filemgr.get_source_content(name)
		if len(source_lines) == 0:
			return Article("None", [], [], "", "")

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
		return Article(json['Title'], json['Parents'], json['Children'], json['Date'], source_markdown)

	def get_frontmatter_json(self, article):
		s = '","'
		return '{\n' \
		+ '"Title": "' + article.title + '",\n' \
		+ '"Abstract": "", \n' \
		+ '"Parents": ["' + s.join([p for p in article.parents]) + '"], \n' \
		+ '"Children": ["' + s.join([c for c in article.children]) + '"], \n' \
		+ '"Date": "' + article.publication_date + '" \n' \
		+ '}'

	def save_article(self, article):
		content = self.get_frontmatter_json(article) + "\n" + article.content
		self.filemgr.set_source_content(article.title, content)


class FileManager:
	def __init__(self, inputFolder, outputFolder, templatesFolder):
		self.source_folder = inputFolder
		self.source_extension = ".md"
		self.template_location = templatesFolder
		self.render_folder = outputFolder
		self.render_extension = ".html"
		self.template_name = "page_template.html"
		self.template_map = "map_template.html"
		self.template_news = "news_template.html"
		self.change_register = filechanges.FileChangeRegister(outputFolder)
		self.file_filters = [".DS_Store"]


	def apply_filter(self, source_file):
		for filt in self.file_filters:
			if filt in source_file:
				return False
		return True

	def list_source(self):
		raw_source_files = []
		for (dirpath, dirnames, filenames) in walk(self.source_folder):
			raw_source_files.extend(filenames)

		names = []
		for f in raw_source_files:
			if self.apply_filter(self.source_folder + f):
				names.append(f[:-len(self.source_extension)])

		return names

	def list_changed_source(self):
		sources = self.list_source()
		return [f for f in sources if self.change_register.has_changed(self.get_full_path(f))]

	def exists(self, name):
		return path.exists(self.get_full_path(name))

	def get_full_path(self, name):
		return self.source_folder + name + self.source_extension

	def get_source_content(self, name):
		if not path.exists(self.get_full_path(name)):
			return ['']
		with open(self.get_full_path(name), "r") as file:
			return file.readlines()

	def set_source_content(self, name, content):
		with open(self.get_full_path(name), "w") as file:
			file.write(content)

	def save_output(self, name, content):
		with open(self.render_folder + name + self.render_extension, "w") as file:
			file.write(content)
		self.change_register.update(self.get_full_path(name))





# The SourceLinker class handles the creation of new child source files
# as well as checks and updates the links between articles to keep them up-to-date.
class FileLinker:
	def __init__(self, filemgr, article_reader):
		self.filemgr = filemgr
		self.article_reader = article_reader
		self.open_editor_on_create = True

	def create_empty_source_file(self, title, parents):
		d = date.today().strftime("%Y-%m-%d")
		article = Article(title, parents, [], d, '# ' + title)
		self.article_reader.save_article(article)

	def open_editor(self, title):
		filename = self.filemgr.get_full_path(title)
		os.system('subl "' + filename + '"')

	# Create new, missing files
	def create_new_files(self):
		display("Scanning for new children...")
		new_articles = []
		for title in self.filemgr.list_source():
			article = self.article_reader.read_article(title)
			for child_title in article.children:
				if child_title == "":
					continue
				if not self.filemgr.exists(child_title):
					self.create_empty_source_file(child_title, [title])
					new_articles.append(child_title)
					display('- Created new children: ' + child_title)
			if len(article.parents) == 0:
				continue
			for parent_title in article.parents:
				if parent_title == '':
					continue
				if not self.filemgr.exists(parent_title):
					self.create_empty_source_file(parent_title, [])
					new_articles.append(parent_title)
					display('- Created new parent: ' + parent_title)

		if self.open_editor_on_create:
			if len(new_articles) != 0:
				display('Opening new files...')
			for article in new_articles:
				self.open_editor(article)


	def update_missing_links(self):
		self.update_parents()
		self.update_children()

	# Updates missing parents
	def update_parents(self):
		display("Updating missing parents...")
		for title in self.filemgr.list_source():
			article = self.article_reader.read_article(title)
			for child_title in article.children:
				if child_title == '':
					continue
				child = self.article_reader.read_article(child_title)
				if not title in child.parents:
					child.parents.append(title)
					self.article_reader.save_article(child)
					display('- Updated ' + child.title + ' with missing parent: ' + title)

	# Updates missing children
	def update_children(self):
		display("Updating missing children...")
		for title in self.filemgr.list_source():
			article = self.article_reader.read_article(title)
			for parent_title in article.parents:
				if parent_title == '':
					continue

				parent = self.article_reader.read_article(parent_title)
				if not title in parent.children:
					parent.children.append(title)
					self.article_reader.save_article(parent)
					display('- Updated ' + parent.title + ' with missing children: ' + title)