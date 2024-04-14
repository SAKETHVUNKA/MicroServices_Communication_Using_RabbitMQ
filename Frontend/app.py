from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/healthcheck")
def healthcheck():
    return render_template("healthcheck.html")

@app.route("/additem")
def additem():
    return render_template("additem.html")

@app.route("/edititem")
def edititem():
    # get item ID and do stuff
    return render_template("edititem.html")

@app.route("/stockmanagement")
def stockmanagement():
    return render_template("stockmanagement.html")

@app.route("/addorder")
def addorder():
    return render_template("addorder.html")

@app.route("/ordertracking")
def ordertracking():
    return render_template("ordertracking.html")

app.run(port=8000, debug=True)