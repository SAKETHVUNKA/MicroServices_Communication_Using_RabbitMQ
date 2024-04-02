from flask import Flask, jsonify, request
import pika

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

# Declare queues for sending message 
channel.queue_declare(queue='health_check_queue')
channel.queue_declare(queue='order_processing_queue')
channel.queue_declare(queue='create_item_queue')
channel.queue_declare(queue='stock_management_queue')

# Declare queues for receiving messages
channel.queue_declare(queue='health_check_response')
channel.queue_declare(queue='order_processing_response')
channel.queue_declare(queue='create_item_response')
channel.queue_declare(queue='stock_management_response')

def publish_message(queue_name, message):
    global channel
    if channel is None or not channel.is_open:
        channel = get_channel()
    if channel:
        try:
            channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        except pika.exceptions.StreamLostError:
            print("Connection to RabbitMQ lost. Reconnecting...")
            channel = get_channel()
            if channel:
                channel.basic_publish(exchange='', routing_key=queue_name, body=message)
            else:
                print("Failed to reconnect to RabbitMQ. Message not sent.")
    else:
        print("Failed to establish connection to RabbitMQ. Message not sent.")

@app.route('/health_check', methods=['POST'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'Consumer is healthy'})

@app.route('/order_processing', methods=['POST'])
def order_processing():
    data = request.json
    publish_message('order_processing_queue', 'Order Processing: ' + str(data))
    return jsonify({'message': 'Order processing request sent to RabbitMQ'})

@app.route('/create_item', methods=['POST'])
def create_item():
    data = request.json
    publish_message('create_item_queue', 'Create Item: ' + str(data))
    return jsonify({'message': 'Item creation request sent to RabbitMQ'})

@app.route('/stock_management', methods=['POST'])
def stock_management():
    data = request.json
    publish_message('stock_management_queue', 'Stock Management: ' + str(data))
    return jsonify({'message': 'Stock management request sent to RabbitMQ'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)