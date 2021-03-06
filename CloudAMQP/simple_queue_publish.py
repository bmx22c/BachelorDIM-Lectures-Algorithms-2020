import pika
import os
import keys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--concurrency", "-C", action="store_true")
args = parser.parse_args()

print(args.concurrency)

def sendMessage(message = "Hello World"):
    '''
    Send message using MQTT

    Parameters:
        message: the message you want to send (default = "Hello World")
    '''
    url = os.environ.get('CLOUDAMQP_URL', keys.amqpkey)
    params = pika.URLParameters(url)
    params.socket_timeout = 5

    message = "Hello World!"

    # publish
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='presentation')

    # channel.basic_publish(exchange='',
    #     routing_key='presentation',
    #     body=message)

    for i in range(0, 100):
        if args.concurrency:
            channel.basic_publish(exchange='',
            routing_key='presentation',
            body=message+str(i),
            properties=pika.BasicProperties(
                delivery_mode=2
            ))
            print(" [X] Send '"+message+str(i)+"'")
        else:
            channel.basic_publish(exchange='',
            routing_key='presentation',
            body=message+str(i))
            print(" [X] Send '"+message+str(i)+"'")


    connection.close()

sendMessage()