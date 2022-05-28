import hashlib
import os
import json

# Data representing the state of a file (source / destination)
class FileState:
	def __init__(self, source, destination, source_hash, destination_hash) -> None:
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

	def get(self, source, destination):
		src_hash = self.compute_hash(source)
		dst_hash = self.compute_hash(destination)
		return FileState(source, destination, src_hash, dst_hash)

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
				states[s] = FileState(state_dict['source'], state_dict['destination'], state_dict['source_hash'], state_dict['destination_hash'])
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
	
	def get_deleted(self, all_names):
		return list(filter(lambda x: x not in all_names, self.states))

# Monitors files states
class FileStateMonitor:
	def __init__(self, database, destination_folder) -> None:
		self.database = database
		self.destination_folder = destination_folder
		self.state_getter = FileStateGetter()

	def get_destination(self, source):
		dest = os.path.join(self.destination_folder, os.path.basename(source).replace('.md', '') + ".html")
		return dest

	def has_changed(self, name):
		if not self.database.exists(name):
			return True

		last_state = self.database.get(name)
		current_state = self.state_getter.get(last_state.source, last_state.destination)
		return last_state.source_hash != current_state.source_hash or last_state.destination_hash != current_state.destination_hash

	def update(self, name, source_filename):
		if not self.state_getter.exists(source_filename) and self.database.exists(name):
			self.database.remove(name)
			return

		current_state = self.state_getter.get(source_filename, self.get_destination(source_filename))
		self.database.update(name, current_state)
	
	def get_changed_files(self, all_names):
		deleted = self.database.get_deleted(all_names)
		existing_files = filter(lambda x: x not in deleted, all_names)
		changed = list(filter(lambda x: self.has_changed(x), existing_files))
		return deleted + changed

	def remove(self, name):
		self.database.remove(name)