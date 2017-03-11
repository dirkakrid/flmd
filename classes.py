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
		with open(file) as config_obj:
			data = json.load(config_obj)

		self.data = data
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

class Filename:
	def __init__(self, url):
		self.file = ''

		if url.endswith('/'):
			if file_exists(self.file_path('index')):
				self.file = self.file_path('index')
			elif file_exists(self.file_path(url)):
				self.file = self.file_path(url)
		else:
			if file_exists(self.file_path(url)):
				self.file = self.file_path(url)
			elif file_exists(self.file_path('index')):
				self.file = self.file_path('index')

	def file_path(self, name):
		# returns full file name, content_dir, file_name, file_ext
		content_dir = append_char(config('content.dir').data, '/')
		file_name = append_char(name, prepend_char(config('content.ext').data, '.'))
		return content_dir + file_name

class Content:
	def __init__(self, file_path):
		self.content = self.get_file_content(file_path)
		self.args = {}
		self.compiled = self.parse_md(self.content)

	def get_file_content(self, file_path):
		with open(file_path, 'r') as file_obj:
			file_content = file_obj.read()
		return file_content

	def parse_md(self, content):
		return Markup(markdown.markdown(content))

class Theme:
	def __init__(self, template=None):
		self.dir = os.path.abspath(config('themes.dir').data)
		themes_dir = append_char(config('themes.dir').data, '/')
		self.path = self.theme_path()
		self.config = self.theme_config(themes_dir + self.path)

		if template != None and file_exists(themes_dir + self.template_path(template)):
			self.template = self.template_path(template)
		elif file_exists(themes_dir + self.template_path('index')):
			self.template = self.template_path('index')
		else:
			self.template = ''

	def theme_path(self):
		return append_char(config('themes.current').data, '/')

	def theme_config(self, path):
		if file_exists(path + 'config.json'):
			config_file = path + 'config.json'
			return config(file=config_file).data
		else:
			return {}

	def template_path(self, name):
		# returns full file name, content_dir, file_name, file_ext
		file_name = name + prepend_char(self.config.get('ext'), '.')
		return self.path + file_name