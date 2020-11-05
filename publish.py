from os import walk
from os import path
import shutil
import json

# This script publishes the results into the publish directory
# Using a json file publish-settings.json at the root of the repository
# Content: 
# { "publish-to": "/path/to/destination/" }

with open('publish-settings.json', "r") as file:
	publish_settings = json.loads(file.read())

output_folder = "output/"
publish_to = publish_settings['publish-to']
print('Publishing to ' + str(publish_to))

published_files = []
for (dirpath, dirnames, filenames) in walk(output_folder):
	published_files.extend(filenames)
	break

for file in published_files:
	shutil.copy(path.join(output_folder, file), publish_to)
	print("Updated " + file)
