from flask import Flask, jsonify, render_template, url_for
import json
import pika
import requests

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

@app.route("/sellitem")
def sellitem():
    # get item ID and do stuff
    return render_template("sellitem.html")

@app.route("/stockmanagement")
def stockmanagement():
    def send_stockmanagement_request(operation_type):
        url = "http://0.0.0.0:5555/stock_management"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'operation_type': operation_type
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.text

    # Get the response for a particular correlation_id
    def get_stockmanagement_response(correlation_id):
        url = "http://localhost:5555/response"
        headers = {'Content-Type': 'application/json'}
        payload = {'correlation_id': correlation_id}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    correlation_id = send_stockmanagement_request("fetch_all")
    print("Request sent. Correlation ID:", correlation_id)

    # Wait for a response
    response = None
    while response is None:
        response = get_stockmanagement_response(correlation_id)
        
    print("Response received:", response) 

    return render_template("stockmanagement.html")

@app.route("/addorder")
def addorder():
    return render_template("addorder.html")

@app.route("/ordertracking")
def ordertracking():
    return render_template("ordertracking.html")

app.run(port=8000, debug=True)