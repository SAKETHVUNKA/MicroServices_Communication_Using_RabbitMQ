import pika
import mysql.connector
import json

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

def fetch_all_order_details(correlation_id):
    mysql_cursor.execute("SELECT * FROM Orders")
    orders = mysql_cursor.fetchall()
    response = {'orders': orders, 'correlation_id': correlation_id}
    # return json.dumps(response
    return json.dumps(response, indent=4, default=str)

def fetch_order_items(order_id, correlation_id):
    mysql_cursor.execute("SELECT * FROM Order_Items WHERE order_id = %s", (order_id,))
    order_items = mysql_cursor.fetchall()
    response = {'order_id': order_id, 'order_items': order_items, 'correlation_id': correlation_id}
    return json.dumps(response, indent=4, default=str)

def create_order(order_data, correlation_id):
    try:
        # Parse JSON data
        # order_data = json.loads(order_data)
        # Extract order details
        order_date = order_data.get('order_date')
        delivery_date = order_data.get('delivery_date', None)
        total_price = order_data.get('total_price')
        status = order_data.get('status', 'placed')
        order_items = order_data.get('order_items', [])

        # Insert order into database
        mysql_cursor.execute("INSERT INTO Orders (order_date, delivery_date, total_price, status) VALUES (%s, %s, %s, %s)",
                             (order_date, delivery_date, total_price, status))
        mysql_connection.commit()
        # Get the order ID of the newly inserted order
        order_id = mysql_cursor.lastrowid

        # Insert order items into database
        for item in order_items:
            product_id = item['product_id']
            quantity = item['quantity']
            unit_price = item['unit_price']
            select_query = f"SELECT * FROM Products WHERE product_id = %s"
            mysql_cursor.execute(select_query, (product_id,))
            existing_data = mysql_cursor.fetchone()
            name = existing_data[1]
            if int(existing_data[6]) < int(quantity):
                response = {'status': 'failure', 'message': f'Insufficient quantity of product: {name}', 'correlation_id': correlation_id}
            else:
                mysql_cursor.execute("INSERT INTO Order_Items (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)",(order_id, product_id, quantity, unit_price))
                final_quantity = int(existing_data[6]) - int(quantity)
                update_query = "UPDATE Products SET current_stock = %s WHERE product_id = %s"
                update_values = [final_quantity,product_id]
                mysql_cursor.execute(update_query, tuple(update_values))
                mysql_connection.commit()
                response = {'status': 'success', 'message': 'Order created successfully.', 'correlation_id': correlation_id}
        return json.dumps(response, indent=4, default=str)
    except Exception as e:
        print("Here?")
        response = {'status': 'failure', 'message': str(e), 'correlation_id': correlation_id}
        return json.dumps(response)

def edit_order(order_id, status, correlation_id):
    try:
        if status:
            mysql_cursor.execute("UPDATE Orders SET status = %s WHERE order_id = %s",(status, order_id))
            mysql_connection.commit()

            # If status is "cancelled" or "rejected", increase stock levels
            if status.lower() == "cancelled" or status.lower() == "rejected":
                # Retrieve order items to increment stock levels
                mysql_cursor.execute("SELECT product_id, quantity FROM Order_Items WHERE order_id = %s", (order_id,))
                order_items = mysql_cursor.fetchall()
                for item in order_items:
                    product_id = item[0]
                    quantity = item[1] 
                    # Increment stock level for each product
                    mysql_cursor.execute("UPDATE Products SET current_stock = current_stock + %s WHERE product_id = %s",
                                         (quantity, product_id))
                mysql_connection.commit()

            response = {'status': 'success', 'message': 'Order status updated successfully.', 'correlation_id': correlation_id}
        else:
            response = {'status': 'failure', 'message': 'No status provided for update.', 'correlation_id': correlation_id}
    except Exception as e:
        response = {'status': 'failure', 'message': str(e), 'correlation_id': correlation_id}
    finally:
        return json.dumps(response)

def order_processing_consumer(ch, method, properties, body):
    request = json.loads(body)
    correlation_id = request.get('correlation_id')
    request_type = request.get('type', None)
    if request_type == 'fetch_all_order_details':
        orders = fetch_all_order_details(correlation_id)
    elif request_type == 'create_order':
        orders = create_order(request['data'], correlation_id)
    elif request_type == 'edit_order':
        order_id = request['order_id']
        status = request['status']
        orders = edit_order(order_id, status, correlation_id)
    elif request_type == 'fetch_order_items':
        order_id = request['order_id']
        orders = fetch_order_items(order_id, correlation_id)
    else:
        orders = json.dumps({'status': 'failure', 'message': 'Invalid request type.', 'correlation_id': correlation_id})

    ch.basic_publish(exchange='', routing_key="producer_queue", body=orders)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callback(ch, method, properties, body):
    order_processing_consumer(ch, method, properties, body)

# Consume messages from the queue with manual acknowledgment
channel.basic_consume(queue='order_processing_queue', on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()