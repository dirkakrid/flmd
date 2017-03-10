from flask import Flask, abort, render_template, Markup
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

def get_md_from_file(file):
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
		output = get_md_from_file(file_name.format(file + 'index'))
	else:
		output = get_md_from_file(file_name.format(file))
		if output == None:
			output = get_md_from_file(file_name.format(file + '/index'))
	return render_template('index.html', content=Markup(output)) if output is not None else abort(404)


@app.errorhandler(404)
def err_404(e):
	content = get_md_from_file(config('content_dir').data + '404' + config('ext').data)
	output = render_template('index.html', content=Markup(content))
	return output if content is not None else '404'

if __name__ == "__main__":
	app.run()