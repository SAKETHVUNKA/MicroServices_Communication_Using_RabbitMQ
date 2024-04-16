from flask import Flask, jsonify, render_template, url_for, request, redirect
import json
import pika
import requests

app = Flask(__name__)

##################################################################################################

@app.route("/")
def home():
    return render_template("home.html")

##################################################################################################

@app.route("/healthcheck")
def healthcheck():
    return render_template("healthcheck.html")

##################################################################################################

@app.route("/additem", methods=["GET", "POST"])
def additem():
    if request.method == 'POST':

        def send_additem_request(operation_type):
            url = "http://0.0.0.0:5555/create_item"
            headers = {'Content-Type': 'application/json'}
            payload = {
                'operation_type': operation_type,

                'name': request.form['itemName'],
                'description': request.form['description'],
                'category': request.form['category'],
                'unit_price': request.form['sellingPrice'],
                'cost_price': request.form['purchasePrice'],
                'current_stock': request.form['quantity'],
                'company': request.form['company'],
                'image': request.form['imageUpload'],
                'date_of_manufacture': request.form['dateManufacture'],
                'date_of_expiry': request.form['useBy'],
                'supplier_id': request.form['distributor'],
                'reorder_level': 0,

                # 'placeManufacture': request.form['placeManufacture'],
            }

            response = requests.post(url, json=payload, headers=headers)
            return response.text

        def get_additem_response(correlation_id):
            url = "http://localhost:5555/response"
            headers = {'Content-Type': 'application/json'}
            payload = {'correlation_id': correlation_id}
            response = requests.post(url, json=payload, headers=headers)
            return response.json()

        correlation_id = send_additem_request("create_order")
        print("Request sent. Correlation ID:", correlation_id)

        # Wait for a response
        response = None
        while response is None:
            response = get_additem_response(correlation_id)
            
        # print("Response received:", response)
        return redirect(url_for('home'))
        
    # GET
    return render_template("additem.html")

##################################################################################################

@app.route("/edititem/<product_id>", methods=["GET", "POST"])
def edititem(product_id):
    if request.method == 'POST':

        def send_edititem_request(operation_type):
            url = "http://0.0.0.0:5555/stock_management"
            headers = {'Content-Type': 'application/json'}
            payload = {
                'operation_type': operation_type,
                'product_id': product_id,

                'new_data': {
                    'name': request.form['itemName'],
                    'description': request.form['description'],
                    'category': request.form['category'],
                    'unit_price': request.form['sellingPrice'],
                    'cost_price': request.form['purchasePrice'],
                    'current_stock': request.form['quantity'],
                    'company': request.form['company'],
                    'image': request.form['imageUpload'],
                    'date_of_manufacture': request.form['dateManufacture'],
                    'date_of_expiry': request.form['useBy'],
                    'supplier_id': request.form['distributor'],
                    'reorder_level': 0,

                    # 'distributor': request.form['distributor'],
                }
            }

            print(payload)
            response = requests.post(url, json=payload, headers=headers)
            return response.text

        def get_edititem_response(correlation_id):
            url = "http://localhost:5555/response"
            headers = {'Content-Type': 'application/json'}
            payload = {'correlation_id': correlation_id}
            response = requests.post(url, json=payload, headers=headers)
            return response.json()

        correlation_id = send_edititem_request("modify")
        print("Request sent. Correlation ID:", correlation_id)

        # Wait for a response
        response = None
        while response is None:
            response = get_edititem_response(correlation_id)
            
        print("Response received:", response)

    return render_template("edititem.html", product_id=product_id)

##################################################################################################

@app.route("/sellitem")
def sellitem():
    # get item ID and do stuff
    return render_template("sellitem.html")

##################################################################################################

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
        
    # print("Response received:", response)
    # print(response["stock_data"])

    return render_template("stockmanagement.html", dataDict = response["stock_data"])

##################################################################################################

@app.route("/addorder")
def addorder():
    return render_template("addorder.html")

##################################################################################################

@app.route("/ordertracking")
def ordertracking():
    def send_ordertracking_request(operation_type):
        url = "http://0.0.0.0:5555/order_processing"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'type': operation_type
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.text

    # Get the response for a particular correlation_id
    def get_ordertracking_response(correlation_id):
        url = "http://localhost:5555/response"
        headers = {'Content-Type': 'application/json'}
        payload = {'correlation_id': correlation_id}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    correlation_id = send_ordertracking_request("fetch_all_order_details")
    print("Request sent. Correlation ID:", correlation_id)

    # Wait for a response
    response = None
    while response is None:
        response = get_ordertracking_response(correlation_id)

    return render_template("ordertracking.html", dataList = response['orders'])

##################################################################################################

@app.route("/changestatus/<order_id>", methods=["GET","POST"])
def change_status(order_id):
    if request.method == 'POST':

        def send_changestatus_request(operation_type):
            url = "http://0.0.0.0:5555/order_processing"
            headers = {'Content-Type': 'application/json'}
            payload = {
                'type': operation_type,
                'order_id': order_id,
                'status': request.form['status'],
            }
            response = requests.post(url, json=payload, headers=headers)
            return response.text

        # Get the response for a particular correlation_id
        def get_changestatus_response(correlation_id):
            url = "http://localhost:5555/response"
            headers = {'Content-Type': 'application/json'}
            payload = {'correlation_id': correlation_id}
            response = requests.post(url, json=payload, headers=headers)
            return response.json()

        correlation_id = send_changestatus_request("edit_order")
        print("Request sent. Correlation ID:", correlation_id)

        # Wait for a response
        response = None
        while response is None:
            response = get_changestatus_response(correlation_id)

        print("Response received:", response)

        return redirect(url_for("ordertracking"))

    return render_template("changestatus.html", order_id = order_id)

##################################################################################################

@app.route("/display_items/<order_id>")
def display_items(order_id):

    def send_display_items_request(operation_type):
        url = "http://0.0.0.0:5555/order_processing"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'order_id': order_id,
            'type': operation_type
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.text

    # Get the response for a particular correlation_id
    def get_display_items_response(correlation_id):
        url = "http://localhost:5555/response"
        headers = {'Content-Type': 'application/json'}
        payload = {'correlation_id': correlation_id}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    correlation_id = send_display_items_request("fetch_order_items")
    print("Request sent. Correlation ID:", correlation_id)

    # Wait for a response
    response = None
    while response is None:
        response = get_display_items_response(correlation_id)
        
    # print("Response received:", response)

    return render_template("display_order_items.html", dataList=response["order_items"])

##################################################################################################

app.run(port=8000, debug=True)