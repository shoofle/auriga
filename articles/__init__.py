"""Route requests for articles according to shoofle's rules.

This is a simple module which is basically entirely here to provide access, in a sensible location,
to the `bloop` object. It's a blueprint which describes how to route requests for articles on my website
(possibly located at http://shoofle.net, possibly not located there). Most of the interesting stuff is in
`render_article`; Go team!"""

import os
from flask import Blueprint, render_template, abort

folder = "articles"
article_base_template = os.path.join(folder, "article.template.html")
bloop = Blueprint("articles", __name__, template_folder="")

@bloop.route("/")
def main_page():
	"""Renders the list of articles/projects."""
	return render_template("project_list.html")

@bloop.route("/raw/<path:page_name>/")
def render_file(page_name):
	"""Does nothing. Not really sure why I have this."""
	file_name = os.path.join(folder, page_name.replace("-", "_"))
	
@bloop.route("/<page_name>/")
def render_article(page_name):
	"""Renders a requested article! This should always be @routed last, because it catches a 
	wide variety of requests. As a result, other things need to be @routed first, because they 
	might never get called if this catches them first."""
	# Arguably, the various options for how to render (templates, articles, flat html) could be stuck into various 
	# subdirectories. Ultimately I don't want to do this because I want this to be lightweight - this __init__.py file 
	# can be chucked into any folder and start showing pages correctly. But whatever!

	# In the examples, let's think about a request for "example.com/some-article".

	# First, we convert the important part of the requested page into a filename
	# "example.com/Some-Article/" => folder="Some-Article" => file_name = "articles/some_article"
	file_name = os.path.join(folder, page_name.replace("-", "_").lower())

	# Here's the priority list for file rendering!
	if os.path.isfile(file_name + ".template.html"):
		# If the file "articles/some_article.template.html" exists, then there's a specific {template} written 
		# for this path. Specific page {templates} take priority.
		return render_template(file_name + ".template.html")
	if os.path.isfile(file_name + ".article.html"):
		# If "articles/some_article.article.html" exists but there's no template, then we should render that
		# {article fragment}, but using the {article base template}. In the future, this should possibly also
		# extract the title from the {article fragment} and feed it into the {article base template} as well.
		return render_template(article_base_template, target=file_name + ".article.html")
	if os.path.isfile(file_name + ".html"):
		# If we haven't found any results yet, check to see if "articles/some_article.html" exists. If it does,
		# just display it plain. This also provides a clean way to access the raw form of files like
		# "articles/some_article.template.html" - just make a request for "example.com/some-article.template/"
		# and it will be caught by this rule and rendered.
		return render_template(file_name + ".html")
	if os.path.isfile(file_name):
		# If it didn't match any other rules, then just render the file that has precisely the requested name.
		return render_template(file_name);

	# I *believe* there's one instance that can't be accessed by this kind of routing in any way:
	# If the files "articles/some_article" and "articles/some_article.html" both exist, then no request will
	# convince this blueprint to return the former. However, as sacrifices go, I don't think it's too bad, and 
	# that should be the only case when this happens.

	# If we didn't find any files, throw up a 404.

	abort(404)

"""Th-th-th-that's all, folks!"""