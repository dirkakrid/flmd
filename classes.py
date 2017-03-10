from flask import abort, render_template, Markup
import os, json, markdown

def append_char(string, char):
	return string + char if not string.endswith(char) else string

def prepend_char(string, char):
	return char + string if not string.startswith(char) else string

def file_exists(file):
	if os.path.isfile(file):
		return True
	return False

class config:
	def __init__(self, val=None, file='config.json', delim='.'):
		with open(file) as f:
			data = json.load(f)

		if val != None:
			val = val.split(delim)
			ndata = data
			for item in val:
				if item in ndata:
					ndata = ndata[item]
				else:
					ndata = None
			else:
				self.data = ndata
		else:
			self.data = data

class File:
	def __init__(self, url):
		self.content = ''
		self.file = ''
		if url.endswith('/'):
			if file_exists(self.file_name('index')):
				self.file = self.file_name('index')
			elif file_exists(self.file_name(url)):
				self.file = self.file_name(url)
		else:
			if file_exists(self.file_name(url)):
				self.file = self.file_name(url)
			elif file_exists(self.file_name('index')):
				self.file = self.file_name('index')
		if file_exists(self.file):
			self.get_file_content()
			self.parse_md()
		# abort(404)

	def file_name(self, name):
		# returns full file name, content_dir, file_name, file_ext
		content_dir = append_char(config('content.dir').data, '/')
		file_name = append_char(name, prepend_char(config('content.ext').data, '.'))
		return content_dir + file_name

	def get_file_content(self):
		with open(self.file, 'r') as file_obj:
			file_contents = file_obj.read()
		self.content = file_contents

	def parse_md(self):
		self.content = markdown.markdown(self.content)

class theme:
	def __init__(self):
		self.theme_dir = append_char(config('theme.dir').data, '/')
		self.current_theme = config('theme.current').data
		self.theme_config = config(file=theme_dir+append_char(self.current_theme, '/'))
		print self.theme_config

	def get_template(self, template):
		if file_exists(self.theme_dir + template):
			print 'theme'