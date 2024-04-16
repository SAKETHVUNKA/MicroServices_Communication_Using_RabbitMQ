import pika
import subprocess
import json
# import docker

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672))
channel = connection.channel()

# Establish connection to MySQL database
def check_container_health(container_name):
    try:
        # client = docker.from_env()
        # container_name = 'producer'
        # container = client.containers.get(container_name)
        # return container.status
        return "Closed"
    except Exception as e:
        return f"Error: {e}"

def health_check_consumer(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    request_data = json.loads(body.decode('utf-8'))
    container_name = request_data.get('container_name')
    
    # Extract correlation_id from the request properties
    correlation_id = request_data.get('correlation_id')
    
    health_status = check_container_health(container_name)
    
    # Include correlation_id in the response JSON
    response_data = {
        "health_status": health_status,
        "correlation_id": correlation_id
    }
    
    channel.basic_publish(exchange='', routing_key="producer_queue", body=json.dumps(response_data))

def callback(ch, method, properties, body):
    health_check_consumer(ch, method, properties, body)

# Consume messages from the queue
channel.basic_consume(queue='health_check_queue', on_message_callback=callback, auto_ack=False)

print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()