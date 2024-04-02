import pika
import mysql.connector

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
channel = connection.channel()

# Establish connection to MySQL database (consider using a connection pool)
mysql_connection = mysql.connector.connect(
    host='database',
    port=3306,
    user='root',
    password='mypassword',
    database='cc_project'
)
mysql_cursor = mysql_connection.cursor()

def order_processing_consumer(ch, method, properties, body):
        print("message received: {body}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    order_processing_consumer(ch, method, properties, message)

# Consume messages from the queue with manual acknowledgment
channel.basic_consume(queue='order_processing_queue', on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()