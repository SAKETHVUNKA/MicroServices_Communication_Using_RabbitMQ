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

def fetch_all_stock_data(correlation_id):
    # Query to fetch data of all stocks from the database
    query = "SELECT * FROM Products"
    mysql_cursor.execute(query)
    rows = mysql_cursor.fetchall()

    # Construct JSON object
    stock_data = []
    for row in rows:
        product = {
            'product_id': row[0],
            'name': row[1],
            'description': row[2],
            'category': row[3],
            'unit_price': float(row[4]),
            'cost_price': float(row[5]),
            'current_stock': row[6],
            'company': row[7],
            'image': row[8],
            'reorder_level': row[9],
            'supplier_id': row[10],
            'date_of_manufacture': row[11],
            'date_of_expiry': row[12]
        }
        stock_data.append(product)

    response_data = {
        "stock_data": stock_data,
        "correlation_id": correlation_id
    }

    return json.dumps(response_data)

def modify_stock_particulars(operation, correlation_id):
    # Extract operation details from the JSON body
    product_id = operation.get('product_id')
    new_data = operation.get('new_data')

    try:
        # Get the existing data for the product from the database
        select_query = "SELECT * FROM Products WHERE product_id = %s"
        mysql_cursor.execute(select_query, (product_id,))
        existing_data = mysql_cursor.fetchone()

        # Prepare the update query
        update_query = "UPDATE Products SET "
        update_values = []
        for field in ['name', 'description', 'category', 'unit_price', 'cost_price', 'current_stock', 'company', 'image', 'reorder_level', 'supplier_id', 'date_of_manufacture', 'date_of_expiry']:
            if field in new_data and new_data[field] is not None:
                update_query += f"{field} = %s, "
                update_values.append(new_data[field])
            else:
                update_query += f"{field} = %s, "
                # update_values.append(existing_data[field])
                update_values.append(existing_data[existing_data.index(field)])
        update_query = update_query.rstrip(', ') + " WHERE product_id = %s"
        update_values.append(product_id)

        # Execute the update query
        mysql_cursor.execute(update_query, tuple(update_values))
        mysql_connection.commit()

        response_data = {
            "message": "Stock particulars modified successfully.",
            "correlation_id": correlation_id
        }
    except Exception as e:
        response_data = {
            "message": f"Failed to modify stock particulars: {str(e)}",
            "correlation_id": correlation_id
        }

    return json.dumps(response_data)

def stock_management_consumer(ch, method, properties, body):
    # Parse the JSON body
    try:
        operation = json.loads(body)
        correlation_id = operation.get('correlation_id')
        # Check the operation type and call the corresponding function
        if operation.get('operation_type') == 'fetch_all':
            # Fetch all stock data and return as JSON
            stock_data_json = fetch_all_stock_data(correlation_id)
            ch.basic_publish(exchange='', routing_key="producer_queue", body=stock_data_json)
        elif operation.get('operation_type') == 'modify':
            response = modify_stock_particulars(operation, correlation_id)
            ch.basic_publish(exchange='', routing_key="producer_queue", body=response)
        else:
            response_data = {
                "message": "Unknown operation.",
                "correlation_id": correlation_id
            }
            ch.basic_publish(exchange='', routing_key="producer_queue", body=json.dumps(response_data))
    except json.JSONDecodeError:
        response_data = {
            "message": "Invalid JSON format.",
            "correlation_id": correlation_id
        }
        ch.basic_publish(exchange='', routing_key="producer_queue", body=json.dumps(response_data))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callback(ch, method, properties, body):
    stock_management_consumer(ch, method, properties, body)

# Consume messages from the queue
channel.basic_consume(queue='stock_management_queue', on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()