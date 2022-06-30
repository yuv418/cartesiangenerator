from flask import Flask, request, render_template, send_file, jsonify, flash, redirect, url_for
from dataclasses import dataclass, fields, _MISSING_TYPE
from io import BytesIO
import tempfile
import os
import subprocess


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("GGEN_SKEY") or "testing"
app.jinja_options["block_start_string"] = "<%"
app.jinja_options["block_end_string"] = "%>"
app.jinja_options["comment_start_string"] = "<#"
app.jinja_options["comment_end_string"] = "#>"
app.jinja_options["variable_end_string"] = ">>"
app.jinja_options["variable_start_string"] = "<<"

@dataclass
class GraphParams:
    cols: int
    rows: int
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    margin_left: float = 0.75
    margin_right: float = 0.5
    margin_top: float = 0.5
    margin_bottom: float = 0.5
    x_scale: int = 1
    y_scale: int = 1

# full of dodgy hacks
@app.route("/")
def index():
    gfields=fields(GraphParams)
    # autofill
    """for f in gfields: 
        print(type(f.default))"""

    for i in range(len(gfields)):
        field_name = gfields[i].name 
        if field_name in request.values:
            gfields[i].default = request.values.get(field_name)

    return render_template("index.html", gfields=gfields, type_fn=type, missing_type=_MISSING_TYPE)


def error_msg(msg, json=False):
    # if not json then index
    if json:
        return jsonify({'msg': msg}), 400
    else:
        flash(msg)
        return redirect(url_for('index', **request.values))

@app.route("/graph")
def graph():
    required_params = ["x_min", "x_max", "y_min", "y_max", "cols", "rows"]
    json = False if request.referrer else True # if the referer is even set then we will flash instead of jsonify

    for required_param in required_params:
        if not request.values.get(required_param):
            return error_msg(f"missing param {required_param}", json=json)
        # all are numbers so whatever this is good enough
        # smh python enforce your typing
        if not float(request.values.get(required_param)):
            return error_msg(f"missing param {required_param}", json=json)

    graph_params = GraphParams(**request.values)

    tex_data = render_template(
            "graph.tex.jinja2", params=graph_params)
    tmp_dir_name = ""

    # this is a bad hack to get a temp file name (latex appends .pdf to this)
    with tempfile.NamedTemporaryFile() as tmp:
        pdf_name = os.path.basename(tmp.name)
        tmp_dir_name = os.path.dirname(tmp.name)

        # so efficient
        latexcmd = ['lualatex', f'--output-directory={tmp_dir_name}', f'--jobname={pdf_name}', ]
        proc = subprocess.Popen(latexcmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate(input=tex_data.encode())

        exitc = proc.wait()
        print(exitc)
        tmp_dir_name = tmp.name

    pdf_data = None
    with open(tmp_dir_name + '.pdf', 'rb') as f:
        pdf_data = BytesIO(f.read())

    print(f"deleting {tmp_dir_name}*")
    os.remove(tmp_dir_name + '.pdf')
    os.remove(tmp_dir_name + '.aux')
    os.remove(tmp_dir_name + '.log')

    return send_file(pdf_data, mimetype='application/pdf', download_name="cartesian_plane.pdf") # make a separate thread to delete the files XD

if __name__ == "__main__":
    app.run()
