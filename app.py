from flask import Flask, abort, render_template, Markup
from preflask import preflask

import os, json, markdown

from classes import *

app = Flask(__name__)

app.threaded = True
app.debug = True

pre = preflask()

@app.route(pre.rule)
def pre_files(file):
    return pre.serve(file)

@app.route('/')
@app.route('/<path:url>')
def index(url='/'):
	filename = Filename(url).file
	content = Content(filename)
	theme = Theme()
	app.template_folder = theme.dir
	return render_template(theme.template, content=content.compiled) if content.compiled is not None else abort(404)

@app.errorhandler(404)
def _404(error):
	return '404', 404

if __name__ == "__main__":
	app.run()