from flask import Flask, abort, render_template, Markup
# from preflask import preflask

import os, json, markdown, frontmatter, sys, jinja2

# forces utf-8 as the default encoding
reload(sys)
sys.setdefaultencoding('utf-8')

from classes import *

app = Flask(__name__)

app.threaded = True
app.debug = config('debug').data or False

plugin = Plugin()
theme = Theme()

app.template_folder = theme.jinja_dir

# pre = preflask()

# @app.route(pre.rule)
# def pre_files(file):
#     return pre.serve(file)

@app.route('/')
@app.route('/<path:url>')
def index(url='/'):
	filename = Filename(url)
	content = Content(filename.file)
	args = Args(content)
	template = Template(content)
	rendered = render_template(template.template, content=Render(content.content).output, **args.args)
	if url == '404':
		return rendered, 404
	return rendered

@app.errorhandler(404)
def _404(error):
	return index('404')

if __name__ == "__main__":
	app.run() #, host='0.0.0.0'