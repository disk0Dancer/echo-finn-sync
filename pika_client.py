from venv import logger

import pika
import json
import logging

from pika_client import *

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
    ]
)

logger = logging.getLogger(__name__)

def log(message):
    logger.info(message)

def create_channel(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    return connection, channel

def send_message(queue_name, message):
    connection, channel = create_channel(queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    connection.close()

def consume_messages(queue_name, callback):
    connection, channel = create_channel(queue_name)
    def on_message(ch, method, properties, body):
        callback(json.loads(body))
        print(f"<-- {queue_name} -- Received message: {body}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_consume(queue=queue_name, on_message_callback=on_message)
    print(f"Listening on {queue_name}...")
    channel.start_consuming()
