from flask import abort, render_template, Markup
import os, sys, json, markdown, frontmatter, re

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
		self.data = {}
		if file_exists(file):
			with open(file) as config_obj:
				data = json.load(config_obj)

			self.data = data
			if type(val) == str:
				sub_dict = data
				for key in val.split(delim):
					sub_dict = sub_dict.get(key)
				else:
					self.data = sub_dict

class Filename:
	def __init__(self, url, child=False):
		self.main_config = config('files').data
		self.file = ''

		if url.endswith('/'):
			if file_exists(self.file_path(url + 'index')):
				self.file = self.file_path(url + 'index')
			elif file_exists(self.file_path(url)):
				self.file = self.file_path(url)
			else:
				if not child:
					abort(404)
		else:
			if file_exists(self.file_path(url)):
				self.file = self.file_path(url)
			elif file_exists(self.file_path(url + '/index')):
				self.file = self.file_path(url + '/index')
			else:
				if not child:
					abort(404)

	def file_path(self, name):
		name = name.lstrip('/') if name.startswith('/') else name
		content_dir = append_char(self.main_config.get('dir'), '/')
		file_name = append_char(name, prepend_char(self.main_config.get('ext'), '.'))
		return content_dir + file_name

class Args:
	def __init__(self, content):
		self.args = content.args
		self.child_pages()

	def child_pages(self):
		children = self.args.get('child_pages')
		self.args['child'] = {0:{}}
		if type(children) == str:
			children = re.split(', | ', children)

			child_content = {0:{}}
			for child in children:
				filename = Filename(child, child=True)
				content = Content(filename.file)
				child_content[children.index(child)] = content.args or {}
				child_content[children.index(child)]['content'] = Render(content.content).output

			self.args.pop('child_pages')
			self.args['child'] = child_content

class Content:
	def __init__(self, file_path):
		data = frontmatter.loads(self.file_contents(file_path))
		self.content = data.content
		self.args = data.metadata

	def file_contents(self, file_path):
		if file_exists(file_path):
			with open(file_path, 'r') as file_obj:
				file_contents = file_obj.read()
			return file_contents
		return ''

class Render:
	def __init__(self, content):
		self.output = Markup(markdown.markdown(content))

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
	def __init__(self, template):
		self.template(template.args.get('template', ''))

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

class Plugins:
	def __init__(self):
		main_config = config('plugins').data
		self.plugin_dir = append_char(main_config.get('dir'), '/')
		self.plugin_list = os.listdir(self.plugin_dir) if os.path.isdir(self.plugin_dir) else []
		self.plugin_list = list(set(['.'.join(x.split('.')[:-1]) for x in self.plugin_list]))
		self.plugin_list.remove('plugin')
		sys.path.insert(0, os.path.abspath(self.plugin_dir))
		self.load()
		sys.path.remove(os.path.abspath(self.plugin_dir))

	def load(self):
		self.plugins = {}
		for plugin in self.plugin_list:
			module = __import__(plugin, fromlist=['*'])
			if hasattr(module, plugin):
				self.plugins[plugin] = getattr(module, plugin)

class event_trigger:
	def __init__(self, event_name, *args, **kwargs):
		for plugin, instance in Plugins().plugins.iteritems():
			getattr(instance(), 'event_handler')(event_name, *args, **kwargs)