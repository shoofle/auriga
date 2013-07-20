import os
from os.path import join, isfile

from flask import Flask, render_template, url_for, redirect, send_from_directory

from articles import bloop

app = Flask(__name__)
app.template_folder = ""
#server_directory = "/home/shoofle/auriga/"
#project_directory = join(server_directory, "pages")
#guitar_directory = join(server_directory, "guitar")

@app.route("/favicon.<extension>")
def favicon(extension=None):
	return send_from_directory(join(app.root_path, "static"), "favicon.png", mimetype="image/png")

@app.route("/guitar_tab/")
@app.route("/guitar_tab/<file_name>")
def guitar_display(file_name=None):
	guitar_files = [ f for f in os.listdir(guitar_directory) if isfile(join(guitar_directory, f)) and "html" not in f ]
	if file_name in guitar_files:
		with open(join(guitar_directory, file_name)) as tab:
			c = unicode(tab.read(), "utf-8")
			return render_template("guitar/render_tab.html", contents=c)
	return render_template("guitar/default.html", guitar_files=guitar_files)

app.register_blueprint(bloop)

if __name__ == "__main__":
	app.debug = True
	app.run()
