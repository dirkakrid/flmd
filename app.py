from flask import Flask, abort, render_template, Markup
from preflask import preflask

import os, json, markdown, frontmatter

from classes import *

app = Flask(__name__)

app.threaded = True
app.debug = True

theme = Theme()
app.template_folder = theme.jinja_dir

pre = preflask()

@app.route(pre.rule)
def pre_files(file):
    return pre.serve(file)

@app.route('/')
@app.route('/<path:url>')
def index(url='/'):
	filename = Filename(url).file
	content = Content(filename)
	template = Template(content.args.get('template'))
	return render_template(template.template, content=content.content, **content.args)

@app.errorhandler(404)
def _404(error):
	return '404', 404

if __name__ == "__main__":
	app.run()