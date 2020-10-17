import os
import json as jsonlib
import markdown

def parse(filename, source_folder):
	source_markdown = ""
	source_json = ""

	with open(source_folder + filename, "r") as file:
		source_lines = file.readlines()

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

	return jsonlib.loads(source_json), source_markdown

def get_children(filename, source_folder):
	if filename == "":
		return []
	json, md = parse(filename, source_folder)
	return json['Children']

def get_parents(filename, source_folder):
	if filename == "":
		return []
	json, md = parse(filename, source_folder)
	return json['Parents']

def save(json, markdown, filename):
	with open(filename, "w") as file:
		jsonlib.dump(json, file)
	with open(filename, "a") as file:
		file.write(markdown)