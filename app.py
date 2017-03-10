from flask import Flask, abort, render_template, Markup
import os, json, markdown

app = Flask(__name__)

app.threaded = True
app.debug = True

def is_file(file_path):
	if os.path.isfile(file_path):
		return True
	return False

def rrmadd(string, delim):
	return string.rstrip(delim) + delim

def lrmadd(string, delim):
	return delim + string.lstrip(delim)

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

class theme:
	def __init__(self):
		self.theme_dir = rrmadd(config('theme.dir').data, '/')
		self.current_theme = config('theme.current').data

	def get_template(self, template):
		if is_file(self.theme_dir + template):
			print 'theme'

class file_parser:
	def __init__(self, file_name):
		self.file_name = file_name

	def get_md_from_file(self):
		if is_file(self.file_name):
			with open(self.file_name, 'r') as file_obj:
				file_contents = file_obj.read()
			return markdown.markdown(file_contents)

@app.route('/')
@app.route('/<path:file>')
def index(file='/'):
	file_name = rrmadd(config('content.dir').data, '/') + '{}' + lrmadd(config('content.ext').data, '.')
	output = None
	if file.endswith('/'):
		output = file_parser(file_name.format(file + 'index')).get_md_from_file()
	else:
		output = file_parser(file_name.format(file)).get_md_from_file()
		if output == None:
			output = file_parser(file_name.format(file + '/index')).get_md_from_file()
	return render_template('index.html', content=Markup(output)) if output is not None else abort(404)

@app.errorhandler(404)
def err_404(e):
	content = file_parser(config('content_dir').data + '404' + config('ext').data).get_md_from_file()
	output = render_template('index.html', content=Markup(content))
	return output if content is not None else '404'

if __name__ == "__main__":
	app.run()