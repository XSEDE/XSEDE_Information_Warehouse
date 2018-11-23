import pika

def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(body)
    print(' ')
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

# credentials = pika.PlainCredentials('username', 'password')
# parameters = pika.ConnectionParameters(credentials=credentials)
parameters = pika.URLParameters('amqp://navarro:jpfnspubsub@info1.dyn.xsede.org:5672/xsede%2F')
connection = pika.BlockingConnection(parameters=parameters)

channel = connection.channel()
channel.basic_consume(on_message, 'glue2.applications')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
