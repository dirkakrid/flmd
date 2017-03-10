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

@app.route('/')
@app.route('/<path:file>')
def index(file=None):
	file = config('content_dir').data + file + config('ext').data
	if os.path.isfile(file):
		with open(file, 'r') as file:
			file = file.read()
		return markdown.markdown(file)
	else:
		abort(404)


@app.errorhandler(404)
def err_404(e):
	return '404', 404

if __name__ == "__main__":
	app.run()