import os
from os.path import join, isfile
from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)
app.template_folder = "."
server_directory = "/home/shoofle/auriga/"
project_directory = join(server_directory, "pages")
guitar_directory = join(server_directory, "guitar")

@app.route("/")
def project_list():
	return render_template("project_list.html")

@app.route("/miscellany/")
def miscellany():
	guitar_files = [ f for f in os.listdir(guitar_directory) if isfile(join(guitar_directory, f)) and "html" not in f ]
	return render_template("pages/miscellany.html", guitar_files=guitar_files)

@app.route("/guitar_tab/")
@app.route("/guitar_tab/<file_name>")
def guitar_display(file_name=None):
	guitar_files = [ f for f in os.listdir(guitar_directory) if isfile(join(guitar_directory, f)) and "html" not in f ]
	if file_name in guitar_files:
		with open(join(guitar_directory, file_name)) as tab:
			c = unicode(tab.read(), "utf-8")
			return render_template("guitar/render_tab.html", contents=c)
	return render_template("guitar/default.html", guitar_files=guitar_files)

@app.route("/<project_name>/")
def unknown_project(project_name="miscellany"):
	for file_name in os.listdir(project_directory):
		if not isfile(join(project_directory, file_name)):
			continue
		if file_name == project_name.replace("-","_") + ".html":
			return render_template("pages/" + file_name)
	else:
		return redirect(url_for('miscellany') + '#' + project_name)

if __name__ == "__main__":
	app.run()
