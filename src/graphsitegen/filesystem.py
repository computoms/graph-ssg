import os
import datetime
import hashlib
import json
from graphsitegen.article import Article
from graphsitegen.article import ArticleFile

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
		db_persistence = FileStateDatabasePersistence(".build/" + str(db_hash))
		db = FileStateDatabase(db_persistence)
		self.state_monitor = FileStateMonitor(db, outputFolder)
		self.file_filters = [".DS_Store"]

	def create_article_file(self, name):
		source = self.disk.join(self.source_folder, name + self.source_extension)
		output = self.disk.join(self.render_folder, name + self.render_extension)
		return ArticleFile(name, source, output)

	def create_template_file(self, name, template_path):
		source = self.disk.join(self.template_location, template_path)
		output = self.disk.join(self.render_folder, name + self.render_extension)
		file = ArticleFile(name, source, output)
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
		os.system('subl "' + filename + '"')

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


# Gets file state
class FileStateGetter:
	def __init__(self) -> None:
		pass

	def compute_hash(self, filename):
		if not os.path.isfile(filename):
			return ""
		return hashlib.md5(open(filename,'rb').read()).hexdigest()

	def get(self, name, source, destination):
		src_hash = self.compute_hash(source)
		dst_hash = self.compute_hash(destination)
		return FileState(name, source, destination, src_hash, dst_hash)

	def exists(self, file):
		return os.path.isfile(file)



# Monitors files states
class FileStateMonitor:
	def __init__(self, database, destination_folder) -> None:
		self.database = database
		self.destination_folder = destination_folder
		self.state_getter = FileStateGetter()

	def has_changed(self, file):
		if not self.database.exists(file.name):
			return True
		if file.is_template:
			return True

		last_state = self.database.get(file.name)
		current_state = self.state_getter.get(last_state.name, last_state.source, last_state.destination)
		return last_state.source_hash != current_state.source_hash or last_state.destination_hash != current_state.destination_hash

	def update(self, file):
		if not self.state_getter.exists(file.source) and self.database.exists(file.name):
			self.database.remove(file.name)
			return

		if file.is_template:
			return

		current_state = self.state_getter.get(file.name, file.source, file.output)
		self.database.update(file.name, current_state)
	
	def get_changed_files(self, all_files):
		deleted_states = self.database.get_deleted_states([f.name for f in all_files])
		deleted_files = [ArticleFile(s.name, s.source, s.destination) for s in deleted_states]
		existing_files = filter(lambda x: x.name not in deleted_files, all_files)
		changed_files = list(filter(lambda x: self.has_changed(x), existing_files))
		return deleted_files + changed_files

	def remove(self, file):
		self.database.remove(file.name)

# Store file states
class FileStateDatabase:
	def __init__(self, persistence) -> None:
		self.persistence = persistence
		self.states = self.persistence.load()

	def exists(self, name):
		return name in self.states

	def get(self, name):
		return self.states[name]

	def update(self, name, state):
		self.states[name] = state
		self.persistence.save(self.states)

	def remove(self, name):
		del self.states[name]
		self.persistence.save(self.states)
	
	def get_deleted_states(self, all_names):
		return [self.states[n] for n in filter(lambda x: x not in all_names, self.states)]


# Persistence to file of the file state database
class FileStateDatabasePersistence:
	def __init__(self, path) -> None:
		self.path = path

	def save(self, states):
		with open(self.path, "w") as f:
			json.dump(states, f, indent=2, cls=FileStateEncoder)
		
	def load(self):
		if not os.path.isfile(self.path):
			return {}
		with open(self.path, "r") as f:
			content = json.load(f)
			states = {}
			for s in content:
				state_dict = content[s]
				states[s] = FileState(state_dict['name'], state_dict['source'], state_dict['destination'], state_dict['source_hash'], state_dict['destination_hash'])
			return states

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

# Data representing the state of a file (source / destination)
class FileState:
	def __init__(self, name, source, destination, source_hash, destination_hash) -> None:
		self.name = name
		self.source = source
		self.destination = destination
		self.source_hash = source_hash
		self.destination_hash = destination_hash

class FileStateEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__
