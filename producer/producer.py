# from flask import Flask, jsonify, request
# import pika
# import threading
# import queue
# import uuid

# app = Flask(__name__)

# def establish_connection():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
#     return connection

# def get_channel():
#     global connection
#     if connection is None or not connection.is_open:
#         connection = establish_connection()
#     return connection.channel() if connection else None

# connection = establish_connection()
# channel = get_channel()

# # Declare queues for sending message 
# channel.queue_declare(queue='health_check_queue')
# channel.queue_declare(queue='order_processing_queue')
# channel.queue_declare(queue='create_item_queue')
# channel.queue_declare(queue='stock_management_queue')

# # Declare queues for receiving messages
# channel.queue_declare(queue='health_check_response')
# channel.queue_declare(queue='order_processing_response')
# channel.queue_declare(queue='create_item_response')
# channel.queue_declare(queue='stock_management_response')

# def publish_message(queue_name, message):
#     channel = get_channel()
#     if channel:
#         channel.basic_publish(exchange='', routing_key=queue_name, body=message)

# def consume_message(queue_name):
#     channel = get_channel()
#     if channel:
#         method_frame, header_frame, body = channel.basic_get(queue_name)
#         if method_frame:
#             channel.basic_ack(method_frame.delivery_tag)
#             return body

# responses = ["health_check_response","order_processing_response","create_item_response","stock_management_response"]
# response_queues = {}
# def response_consumer():
#     while True:
#         for queue_name in responses:
#             response = consume_message(queue_name)
#             if response:
#                 correlation_id = response["correlation_id"]
#                 response_queue = response_queues.get(correlation_id)
#                 if response_queue:
#                     response_queue.put(response)

# response_thread = threading.Thread(target=response_consumer)
# response_thread.daemon = True
# response_thread.start()

# def process_request(queue_name, request_data):
#     correlation_id = str(uuid.uuid4())
#     data = request_data
#     data["correlation_id"] = correlation_id
#     response_queue = queue.Queue()
#     response_queues[correlation_id] = response_queue
#     publish_message(queue_name, data)
#     return correlation_id

# @app.route('/health_check', methods=['POST'])
# def health_check():
#     return process_request('health_check_queue', request.json)

# @app.route('/order_processing', methods=['POST'])
# def order_processing():
#     return process_request('order_processing_queue', request.json)

# @app.route('/create_item', methods=['POST'])
# def create_item():
#     return process_request('create_item_queue', request.json)

# @app.route('/stock_management', methods=['POST'])
# def stock_management():
#     return process_request('stock_management_queue', request.json)

# @app.route('/response', methods=['POST'])
# def handle_response():
#     correlation_id = request.json.get("correlation_id")
#     if correlation_id:
#         response_queue = response_queues.get(correlation_id)
#         if response_queue:
#             response = response_queue.get()
#             del response_queues[correlation_id]
#             return response
#     return jsonify({'error': 'No response found for correlation_id'})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)



# from flask import Flask, jsonify, request
# import pika
# import threading
# import queue
# import uuid
# import json

# app = Flask(__name__)

# def establish_connection():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
#     return connection

# def get_channel():
#     global connection
#     if connection is None or not connection.is_open:
#         connection = establish_connection()
#     return connection.channel() if connection else None

# connection = establish_connection()
# channel = get_channel()

# channel.queue_declare(queue='health_check_queue')
# channel.queue_declare(queue='order_processing_queue')
# channel.queue_declare(queue='create_item_queue')
# channel.queue_declare(queue='stock_management_queue')
# channel.queue_declare(queue='producer_queue')

# def publish_message(queue_name, message):
#     global channel
#     json_data = json.dumps(message)
#     if connection and connection.is_open:
#         channel.basic_publish(exchange='', routing_key=queue_name, body=json_data.encode('utf-8'))
#     else:
#         channel = get_channel()
#         channel.basic_publish(exchange='', routing_key=queue_name, body=json_data.encode('utf-8'))

# def consume_message():
#     global channel
#     method_frame, header_frame, body = channel.basic_get(queue="producer_queue")
#     if method_frame:
#         # print(" [x] Received %r" % body)
#         channel.basic_ack(delivery_tag=method_frame.delivery_tag)
#         return body
#     else:
#         return None

# response_queues = {}
# def response_consumer():
#     while True:
#         response = consume_message()
#         if response:
#             # print("in response consumer : ",response)
#             response_data = json.loads(response)
#             correlation_id = response_data.get("correlation_id")
#             response_queue = response_queues.get(correlation_id)
#             if response_queue:
#                 response_queue.put(response_data)

# response_thread = threading.Thread(target=response_consumer)
# response_thread.daemon = True
# response_thread.start()

# def process_request(queue_name, request_data):
#     correlation_id = str(uuid.uuid4())
#     data = request_data
#     data["correlation_id"] = correlation_id
#     response_queue = queue.Queue()
#     response_queues[correlation_id] = response_queue
#     publish_message(queue_name, data)
#     return correlation_id

# @app.route('/health_check', methods=['POST'])
# def health_check():
#     return process_request('health_check_queue', request.json)

# @app.route('/order_processing', methods=['POST'])
# def order_processing():
#     return process_request('order_processing_queue', request.json)

# @app.route('/create_item', methods=['POST'])
# def create_item():
#     return process_request('create_item_queue', request.json)

# @app.route('/stock_management', methods=['POST'])
# def stock_management():
#     return process_request('stock_management_queue', request.json)

# @app.route('/response', methods=['POST'])
# def handle_response():
#     correlation_id = request.json.get("correlation_id")
#     if correlation_id:
#         response_queue = response_queues.get(correlation_id)
#         if response_queue:
#             response = response_queue.get()
#             del response_queues[correlation_id]
#             return jsonify(response)
#     return jsonify({'error': 'No response found for correlation_id'})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

# Invoke-WebRequest -Uri "http://localhost:5000/response" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"correlation_id": "6ba79046-4747-4440-a62c-c64802b5bb1b"}'
# Invoke-WebRequest -Uri "http://localhost:5000/order_processing" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"data": "your_order_data"}'

from flask import Flask, jsonify, request
import pika
import threading
import queue
import uuid
import json

app = Flask(__name__)

def establish_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
    return connection

def get_channel():
    global connection
    if connection is None or not connection.is_open:
        connection = establish_connection()
    return connection.channel() if connection else None

connection = establish_connection()
channel = get_channel()

channel.queue_declare(queue='health_check_queue')
channel.queue_declare(queue='order_processing_queue')
channel.queue_declare(queue='create_item_queue')
channel.queue_declare(queue='stock_management_queue')
channel.queue_declare(queue='producer_queue')

def publish_message(queue_name, message):
    global channel
    json_data = json.dumps(message)
    if connection and connection.is_open:
        channel.basic_publish(exchange='', routing_key=queue_name, body=json_data.encode('utf-8'))
    else:
        channel = get_channel()
        channel.basic_publish(exchange='', routing_key=queue_name, body=json_data.encode('utf-8'))

def consume_message():
    global channel
    method_frame, header_frame, body = channel.basic_get(queue="producer_queue")
    if method_frame:
        print(" [x] Received %r" % body)
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return body
    else:
        return None

response_queues = {}
def response_consumer():
    while True:
        response = consume_message()
        if response:
            print("in response consumer : ",response)
            response_data = json.loads(response)
            correlation_id = response_data.get("correlation_id")
            response_queue = response_queues.get(correlation_id)
            if response_queue:
                response_queue.put(response_data)

response_thread = threading.Thread(target=response_consumer)
response_thread.daemon = True
response_thread.start()

def process_request(queue_name, request_data):
    correlation_id = str(uuid.uuid4())
    data = request_data
    data["correlation_id"] = correlation_id
    response_queue = queue.Queue()
    response_queues[correlation_id] = response_queue
    publish_message(queue_name, data)
    return correlation_id

@app.route('/health_check', methods=['POST'])
def health_check():
    return process_request('health_check_queue', request.json)

@app.route('/order_processing', methods=['POST'])
def order_processing():
    return process_request('order_processing_queue', request.json)

@app.route('/create_item', methods=['POST'])
def create_item():
    return process_request('create_item_queue', request.json)

@app.route('/stock_management', methods=['POST'])
def stock_management():
    return process_request('stock_management_queue', request.json)

@app.route('/response', methods=['POST'])
def handle_response():
    correlation_id = request.json.get("correlation_id")
    if correlation_id:
        response_queue = response_queues.get(correlation_id)
        if response_queue:
            response = response_queue.get()
            del response_queues[correlation_id]
            return jsonify(response)
    return jsonify({'error': 'No response found for correlation_id'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)