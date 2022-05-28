import hashlib
import os
import json

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

# Data representing the state of a file (source / destination)
class FileState:
	def __init__(self, source, destination, source_hash, destination_hash) -> None:
		self.source = source
		self.destination = destination
		self.source_hash = source_hash
		self.destination_hash = destination_hash

	def compute_hash(filename):
		if not os.path.isfile(filename):
			return ""
		return hashlib.md5(open(filename,'rb').read()).hexdigest()

	def get(source, destination):
		src_hash = FileState.compute_hash(source)
		dst_hash = FileState.compute_hash(destination)
		return FileState(source, destination, src_hash, dst_hash)

class FileStateEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

# Store file states
class FileStateDatabase:
	def __init__(self, persistence) -> None:
		self.persistence = persistence
		self.states = self.persistence.load()

	def exists(self, source_filename):
		return source_filename in self.states

	def get(self, source_filename):
		return self.states[source_filename]

	def update(self, state):
		self.states[state.source] = state
		self.persistence.save(self.states)

# Monitors files states
class FileStateMonitor:
	def __init__(self, database, destination_folder) -> None:
		self.database = database
		self.destination_folder = destination_folder

	def get_destination(self, source):
		dest = os.path.join(self.destination_folder, os.path.basename(source).replace('.md', '') + ".html")
		return dest

	def has_changed(self, source_filename):
		if not self.database.exists(source_filename):
			return True

		current_state = FileState.get(source_filename, self.get_destination(source_filename))
		last_state = self.database.get(source_filename)
		return last_state.source_hash != current_state.source_hash or last_state.destination_hash != current_state.destination_hash

	def update(self, source_filename):
		current_state = FileState.get(source_filename, self.get_destination(source_filename))
		self.database.update(current_state)