import pika
import mysql.connector
import json

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
channel = connection.channel()

# Establish connection to MySQL database
mysql_connection = mysql.connector.connect(
    host='database',
    port='3306',
    user='root',
    password='mypassword',
    database='cc_project'
)
mysql_cursor = mysql_connection.cursor()

def item_creation_consumer(ch, method, properties, body):
    print("Message received: {body}")
    # Decode the incoming JSON message
    message = json.loads(body)
    # Extract item details from the message
    name = message.get('name')
    description = message.get('description')
    category = message.get('category')
    unit_price = message.get('unit_price')
    cost_price = message.get('cost_price')
    current_stock = message.get('current_stock')
    company = message.get('company')
    image = message.get('image')
    date_of_manufacture = message.get('date_of_manufacture')
    date_of_expiry = message.get('date_of_expiry')
    supplier_id = message.get('supplier_id')
    reorder_level = message.get('reorder_level')
    
    # Extract correlation_id from the request properties
    correlation_id = message.get('correlation_id')
    
    try:
        # Insert item details into the database
        sql = "INSERT INTO Products (name, description, category, unit_price, cost_price, current_stock, company, image, reorder_level, supplier_id, date_of_manufacture, date_of_expiry) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, description, category, unit_price, cost_price, current_stock, company, image, reorder_level, supplier_id, date_of_manufacture, date_of_expiry)
        mysql_cursor.execute(sql, val)
        mysql_connection.commit()
        response = "Item inserted into database."
    except mysql.connector.Error as err:
        response = f"Failed to insert item into database: {err}"
    
    # Include correlation_id in the response JSON
    response_data = {
        "message": response,
        "correlation_id": correlation_id
    }
    
    # Publish the response message
    channel.basic_publish(exchange='', routing_key="producer_queue", body=json.dumps(response_data))
    
    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callback(ch, method, properties, body):
    item_creation_consumer(ch, method, properties, body)

# Consume messages from the queue
channel.basic_consume(queue='create_item_queue', on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()