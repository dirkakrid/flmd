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
			if file_exists(self.file_path(url + 'index')):
				self.file = self.file_path(url + 'index')
			elif file_exists(self.file_path(url)):
				self.file = self.file_path(url)
		else:
			if file_exists(self.file_path(url)):
				self.file = self.file_path(url)
			elif file_exists(self.file_path(url + '/' + 'index')):
				self.file = self.file_path(url + '/' + 'index')

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
	def __init__(self):
		self.jinja_dir = os.path.abspath(config('themes.dir').data)
		self.themes_dir = append_char(config('themes.dir').data, '/')
		self.theme_path = append_char(config('themes.current').data, '/')
		self.theme_config()

	def theme_config(self):
		config_file = self.themes_dir + self.theme_path + 'config.json'
		if file_exists(config_file):
			self.config = config(file=config_file).data or {}

class Template:
	def __init__(self, template=''):
		self.template(template)

	def template(self, template_name):
		theme = Theme()
		theme_ext = prepend_char(theme.config.get('ext'), '.')
		default_template = theme.config.get('default_template')

		template_file = theme.theme_path + template_name + theme_ext

		if file_exists(theme.themes_dir + template_file):
			self.template = template_file
		else:
			template_file = theme.theme_path + default_template + theme_ext
			if file_exists(theme.themes_dir + template_file):
				self.template = template_file
			else:
				raise NameError('template not found `{}`'.format(theme.theme_path + template_name + theme_ext))