import os
from flask import Blueprint, render_template, abort
from jinja2.exceptions import TemplatesNotFound

folder = "articles"
bloop = Blueprint("articles", __name__, template_folder="")

@bloop.route("/")
def main_page():
	return render_template("project_list.html")

@bloop.route("/a/<page_name>/")
def apply_base_template(page_name):
	file_name = os.path.join(folder, page_name.replace("-", "_"))
	
@bloop.route("/<page_name>/")
def render_article(page_name):
	# Arguably, the various options for how to render (templates, articles, flat html) could be stuck into various subdirectories.
	# Ultimately I don't want to do this because it's supposed to be lightweight - I should be able to chuck this __init__.py file into
	# any folder and start generating stuff correctly. But whatever!

	# Let's find some test filenames!
	file_name = os.path.join(folder, page_name.replace("-", "_"))
	
	# Is there a template by that name? This list is in the priority order for rendering.
	extensions = [".template.html", ".article.html", ".html", ""]
	
	try:
		return render_template([ file_name + suffix for suffix in extensions ])
	except TemplatesNotFound as e:
		abort(404)