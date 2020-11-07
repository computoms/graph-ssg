from os import walk
import os
from os import path
import shutil
import json

# This script publishes the results into the publish directory
# Using a json file publish-settings.json at the root of the repository
# Content: 
# {
#	"publish_root": "/path/to/publish/root",
#	"folders": [
#		{"source": "output", "destination": ""},
#		{"source": "output/images", "destination": "images"},
# 		{"source": "output/images/articles", "destination": "images/articles"}
#	]
#}

with open('publish-settings.json', "r") as file:
	publish_settings = json.loads(file.read())

publish_root = publish_settings['publish_root']
print('Publishing to ' + str(publish_root))

for folder_publish in publish_settings["folders"]:
	source_folder = folder_publish["source"]
	destination_folder = folder_publish["destination"]
	published_files = []
	for (dirpath, dirnames, filenames) in walk(source_folder):
		published_files.extend(filenames)
		break

	print('Publishing files in ' + source_folder)
	destination_path = path.join(publish_root, destination_folder)
	if not path.exists(destination_path):
		os.makedirs(destination_path)

	for file in published_files:
		source_filename = path.join(source_folder, file)
		destination_filename = path.join(publish_root, destination_folder, file)
		#print("Publishing from " + str(source_filename) + " to " + str(destination_filename))
		shutil.copy2(source_filename, destination_filename)
		print("Updated " + file)
