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

def get_channel(connection):
    if connection is None or not connection.is_open:
        connection = establish_connection()
    return connection.channel() if connection else None

connection = establish_connection()
channel = get_channel(connection)
channel.queue_declare(queue='health_check_queue')
channel.queue_declare(queue='order_processing_queue')
channel.queue_declare(queue='create_item_queue')
channel.queue_declare(queue='stock_management_queue')
channel.queue_declare(queue='producer_queue')
channel.close()
connection.close()

def publish_message(queue_name, message ,channel):
    json_data = json.dumps(message)
    k = True
    while k:
        try :
            channel.basic_publish(exchange='', routing_key=queue_name, body=json_data.encode('utf-8'))
            k = False
        except Exception as e:
            k =True

def consume_message(channel):
    method_frame, header_frame, body = channel.basic_get(queue="producer_queue")
    if method_frame:
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return body
    else:
        return None

response_queues = {}
def response_consumer():
    connection1 = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
    channel1 = connection1.channel()
    while True:
        if not (connection1 and connection1.is_open and channel1):
            channel1.close()
            connection1.close()
            connection1 = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
            channel1 = connection1.channel()

        response = consume_message(channel1)
        if response:
                response_data = json.loads(response)
                correlation_id = response_data.get("correlation_id")
                response_queue = response_queues.get(correlation_id)
                if response_queue is not None :
                    response_queue.put(response_data)

response_thread = threading.Thread(target=response_consumer)
response_thread.daemon = True
response_thread.start()

def process_request(queue_name, request_data, channel):
    correlation_id = str(uuid.uuid4())
    data = request_data
    data["correlation_id"] = correlation_id
    response_queue = queue.Queue()
    response_queues[correlation_id] = response_queue
    publish_message(queue_name, data, channel)
    return correlation_id

@app.route('/health_check', methods=['POST'])
def health_check():
    connection = establish_connection()
    channel = get_channel(connection)
    resp = process_request('health_check_queue', request.json ,channel)
    channel.close()
    connection.close()
    return resp

@app.route('/order_processing', methods=['POST'])
def order_processing():
    connection = establish_connection()
    channel = get_channel(connection)
    resp = process_request('order_processing_queue', request.json, channel)
    channel.close()
    connection.close()
    return resp

@app.route('/create_item', methods=['POST'])
def create_item():
    connection = establish_connection()
    channel = get_channel(connection)
    resp = process_request('create_item_queue', request.json ,channel)
    channel.close()
    connection.close()
    return resp

@app.route('/stock_management', methods=['POST'])
def stock_management():
    connection = establish_connection()
    channel = get_channel(connection)
    resp = process_request('stock_management_queue', request.json ,channel)
    channel.close()
    connection.close()
    return resp

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
    app.run(host='0.0.0.0', port=5000)