from flask import Flask, render_template, request, session
from flask_session import Session

import time

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("notes") is None:
        session['notes']  = []
    if session.get("dates") is None:
        session['dates'] = []
    if  request.method == "POST":
        session["notes"].append(request.form.get("note"))
        t = time.ctime(time.time())
        session["dates"].append(t)

    length = len(session["notes"])
    return render_template("index.html", len=length, notes=session["notes"], date=session["dates"])

@app.route("/delete", methods=["GET"])
def delete():
    restart = False
    delete = False
    if request.method == "GET":
        try:
            index = int(request.args["id"])
            del session['notes'][index]
            del session['dates'][index]
            delete = True
        except  KeyError:
            session['notes']  = []
            session['dates'] =  []
            restart = True

    length = len(session["notes"])
    return render_template("index.html", len=length, notes=session["notes"],  date=session["dates"], delete=delete,  restart=restart)
