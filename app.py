from flask import Flask, abort
import os, json, markdown

app = Flask(__name__)

app.threaded = True
app.debug = True

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

def get_md(file):
	if os.path.isfile(file):
		with open(file, 'r') as file_obj:
			file_contents = file_obj.read()
		return markdown.markdown(file_contents)

@app.route('/')
@app.route('/<path:file>')
def index(file='/'):
	file_name = config('content_dir').data + '{}' + config('ext').data
	output = None
	if file.endswith('/'):
		output = get_md(file_name.format(file + 'index'))
	else:
		output = get_md(file_name.format(file))
		if output == None:
			output = get_md(file_name.format(file + '/index'))
	return output if output is not None else abort(404)


@app.errorhandler(404)
def err_404(e):
	return '404', 404

if __name__ == "__main__":
	app.run()