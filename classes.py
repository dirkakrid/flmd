from flask import abort, render_template, Markup
import os, json, markdown

def append_char(string, char):
	return string + char if not string.endswith(char) else string

def prepend_char(string, char):
	return char + string if not string.startswith(char) else string

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

class file_obj:
	def __init__(self, url):
		if url.endswith('/'):
			if self.file_exists(self.file_name('index')):
				print self.file_name('index')
			elif self.file_exists(self.file_name(url)):
				print self.file_name(url)
		else:
			if self.file_exists(self.file_name(url)):
				print self.file_name(url)
			elif self.file_exists(self.file_name('index')):
				print self.file_name('index')
		# abort(404)

	def file_name(self, name):
		# returns full file name, content_dir, file_name, file_ext
		content_dir = append_char(config('content.dir').data, '/')
		file_name = append_char(name, prepend_char(config('content.ext').data, '.'))
		return content_dir + file_name

	def file_exists(self, file):
		if os.path.isfile(file):
			return True
		return False

	def get_file_contents(self, file):
		with open(file, 'r') as file_obj:
			file_contents = file_obj.read()
		return file_contents