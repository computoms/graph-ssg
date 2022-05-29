from os import system
import datetime
from graphsitegen.article import Article

# The FileLinker class handles the creation of new child source files
# as well as checks and updates the links between articles to keep them up-to-date.
class FileLinker:
	def __init__(self, filemgr, article_reader):
		self.filemgr = filemgr
		self.article_reader = article_reader
		self.open_editor_on_create = True

	def display(self, text):
		print(text)

	def create_empty_source_file(self, title, parents):
		d = datetime.date.today().strftime("%Y-%m-%d")
		article = Article(title, parents, [], d, '# ' + title, '')
		self.article_reader.save_article(article)

	def open_editor(self, title):
		filename = self.filemgr.get_full_path(title)
		system('subl "' + filename + '"')

	# Create new, missing files
	def create_new_files(self):
		self.display("Scanning for new children...")
		new_articles = []
		for file in self.filemgr.list_source():
			article = self.article_reader.read_article(file.name)
			for child_title in article.children:
				if child_title == "":
					continue
				if not self.filemgr.exists(child_title):
					self.create_empty_source_file(child_title, [file.name])
					new_articles.append(child_title)
					self.display('- Created new children: ' + child_title)
			if len(article.parents) == 0:
				continue
			for parent_title in article.parents:
				if parent_title == '':
					continue
				if not self.filemgr.exists(parent_title):
					self.create_empty_source_file(parent_title, [])
					new_articles.append(parent_title)
					self.display('- Created new parent: ' + parent_title)

		if self.open_editor_on_create:
			if len(new_articles) != 0:
				self.display('Opening new files...')
			for article in new_articles:
				self.open_editor(article)


	def update_missing_links(self):
		self.update_parents()
		self.update_children()

	# Updates missing parents
	def update_parents(self):
		self.display("Updating missing parents...")
		for file in self.filemgr.list_source():
			article = self.article_reader.read_article(file.name)
			for child_title in article.children:
				if child_title == '':
					continue
				child = self.article_reader.read_article(child_title)
				if not file.name in child.parents:
					child.parents.append(file.name)
					self.article_reader.save_article(child)
					self.display('- Updated ' + child.title + ' with missing parent: ' + file.name)

	# Updates missing children
	def update_children(self):
		self.display("Updating missing children...")
		for file in self.filemgr.list_source():
			article = self.article_reader.read_article(file.name)
			for parent_title in article.parents:
				if parent_title == '':
					continue

				parent = self.article_reader.read_article(parent_title)
				if not file.name in parent.children:
					parent.children.append(file.name)
					self.article_reader.save_article(parent)
					self.display('- Updated ' + parent.title + ' with missing children: ' + file.name)