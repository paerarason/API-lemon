import pika
connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel()
channel.queue_declare(queue="hello da")
channel.basic_publish(exchange='',routing_key='hello da',body='hello world!')
print(' [x] Sent "hello world" ')
connection.close()
