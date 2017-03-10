from flask import abort, render_template, Markup
import os, json, markdown

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

class file:
	def __init__(self, file_name):
		self.file_name = file_name

	def exists(self):
		if os.path.isfile(self.file_name):
			return True
		return False