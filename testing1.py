import pika
import subprocess
import json

# Establish connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
channel = connection.channel()

def check_container_health(container_name):
    try:
        # Execute the docker inspect command to get the health status of the container
        result = subprocess.run(["docker", "inspect", "--format='{{json .State.Health.Status}}'", container_name], capture_output=True, text=True, check=True)
        health_status = result.stdout.strip()
        return health_status
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def health_check_consumer(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    request_data = json.loads(body.decode('utf-8'))
    container_name = request_data.get('container_name')
    
    # Extract correlation_id from the request properties
    correlation_id = properties.correlation_id
    
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
