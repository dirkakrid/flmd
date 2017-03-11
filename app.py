from flask import Flask, abort, render_template, Markup
import os, json, markdown
from classes import *

app = Flask(__name__)

app.threaded = True
app.debug = True

@app.route('/')
@app.route('/<path:url>')
def index(url='/'):
	filename = Filename(url).file
	content = Content(filename)
	theme = Theme()
	return render_template('index.html', content=content.compiled) if content.compiled is not None else abort(404)

@app.errorhandler(404)
def error_404(err):
	return '404', 404

if __name__ == "__main__":
	app.run()