import os
from graphsitegen.filesystem import filechanges
from graphsitegen import article
import hashlib

class Disk:
	def __init__(self) -> None:
		pass

	def isdir(self, path):
		return os.path.isdir(path)

	def mkdir(self, path):
		os.mkdir(path)

	def join(self, path1, path2):
		return os.path.join(path1, path2)

	def file_exists(self, path):
		return os.path.isfile(path)

	def remove_file(self, path):
		return os.remove(path)

	def write_to_file(self, path, content):
		with open(path, 'w') as f:
			f.write(content)

	def read_file(self, path):
		with open(path, 'r') as f:
			return f.readlines()

	def get_files_recursive(self, path):
		raw_source_files = []
		for (dirpath, dirnames, filenames) in os.walk(path):
			raw_source_files.extend(filenames)
		return raw_source_files

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
		self.disk = Disk()

		# Generate unique name based on outputFolder to register the file changes
		if not self.disk.isdir(".build"):
			self.disk.mkdir(".build")
		db_hash = hashlib.md5(outputFolder.encode('utf-8')).hexdigest()
		db_persistence = filechanges.FileStateDatabasePersistence(".build/" + str(db_hash))
		db = filechanges.FileStateDatabase(db_persistence)
		self.state_monitor = filechanges.FileStateMonitor(db, outputFolder)
		self.file_filters = [".DS_Store"]

	def create_article_file(self, name):
		source = self.disk.join(self.source_folder, name + self.source_extension)
		output = self.disk.join(self.render_folder, name + self.render_extension)
		return article.ArticleFile(name, source, output)

	def create_template_file(self, name, template_path):
		source = self.disk.join(self.template_location, template_path)
		output = self.disk.join(self.render_folder, name + self.render_extension)
		file = article.ArticleFile(name, source, output)
		file.is_template = True
		return file

	def apply_filter(self, source_file):
		for filt in self.file_filters:
			if filt in source_file:
				return False
		return True

	def list_source(self):
		raw_source_files = self.disk.get_files_recursive(self.source_folder)
		files = []
		for f in raw_source_files:
			if self.apply_filter(self.source_folder + f):
				files.append(self.create_article_file(f[:-len(self.source_extension)]))

		return files

	def list_changed_source(self):
		return self.state_monitor.get_changed_files(self.list_source())

	def exists(self, name):
		return self.disk.file_exists(self.disk.join(self.source_folder, name + self.source_extension))

	def get_source_content(self, file):
		if not self.disk.file_exists(file.source):
			return ['']
		return self.disk.read_file(file.source)

	def set_source_content(self, file, content):
		self.disk.write_to_file(file.source, content)

	def save_output(self, file, content):
		self.disk.write_to_file(file.output, content)
		self.state_monitor.update(file)
	
	def delete_article(self, file):
		if self.disk.file_exists(file.output):
			self.disk.remove_file(file.output)
		self.state_monitor.remove(file)


