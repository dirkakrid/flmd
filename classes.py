from flask import abort, render_template, Markup
import os, sys, json, markdown, frontmatter

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

class trigger_event:
	def __init__(self, event_name, params=[]):
		print event_name

class handle_event:
	def __init__(self, event_name, params=[]):
		if hasattr(class_name, event_name):
			pass

class Filename:
	def __init__(self, url):
		self.main_config = config('files').data
		self.file = ''

		trigger_event('get_url', [url])

		if url.endswith('/'):
			if file_exists(self.file_path(url + 'index')):
				self.file = self.file_path(url + 'index')
			elif file_exists(self.file_path(url)):
				self.file = self.file_path(url)
			else:
				trigger_event('404', [])
				abort(404)
		else:
			if file_exists(self.file_path(url)):
				self.file = self.file_path(url)
			elif file_exists(self.file_path(url + '/' + 'index')):
				self.file = self.file_path(url + '/' + 'index')
			else:
				trigger_event('404', [])
				abort(404)

		trigger_event('file', [self.file])

	def file_path(self, name):
		# returns full file name, content_dir, file_name, file_ext
		content_dir = append_char(self.main_config.get('dir'), '/')
		file_name = append_char(name, prepend_char(self.main_config.get('ext'), '.'))
		return content_dir + file_name

class Content:
	def __init__(self, file_path):
		data = frontmatter.loads(self.file_contents(file_path))
		self.raw_content = data.content
		self.args = data.metadata

	def file_contents(self, file_path):
		with open(file_path, 'r') as file_obj:
			file_contents = file_obj.read()
		return file_contents

class Render:
	def __init__(self, template, content):
		self.output = render_template(template.template, content=Markup(markdown.markdown(content.raw_content)), **content.args)

class Theme:
	def __init__(self):
		main_config = config('themes').data
		self.jinja_dir = os.path.abspath(main_config.get('dir'))
		self.themes_dir = append_char(main_config.get('dir'), '/')
		self.theme_path = append_char(main_config.get('current'), '/')
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

class Plugin:
	def __init__(self):
		main_config = config('plugins').data
		self.plugins_dir = append_char(main_config.get('dir'), '/')
		self.plugins = os.listdir(self.plugins_dir) if os.path.isdir(self.plugins_dir) else []