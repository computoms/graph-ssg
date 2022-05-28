import hashlib
import os
import json
import article

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
		deleted_files = [article.ArticleFile(s.name, s.source, s.destination) for s in deleted_states]
		existing_files = filter(lambda x: x.name not in deleted_files, all_files)
		changed_files = list(filter(lambda x: self.has_changed(x), existing_files))
		return deleted_files + changed_files

	def remove(self, file):
		self.database.remove(file.name)