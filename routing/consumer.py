import pika
import sys


class RabbitMQ:

    def __init__(self, host, exchange, routing_key) -> None:
        self._host = host
        self._exchange = exchange
        self._credential = pika.PlainCredentials("admin","admin")
        self._routing_key = routing_key
    
    def callback(self, ch, method, properties, body):
        print("[x] received message %r:%r" % (method.routing_key,body))
    
    def start_consume(self):
        self._channel.basic_consume(queue=self._queue,on_message_callback=self.callback,auto_ack=True)
        print(' [*] Waiting for logs. To exit press CTRL+C')
        self._channel.start_consuming()
    
    def create_connection(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = self._host,
            credentials = self._credential
        ))
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self._exchange,exchange_type="direct")
        res = self._channel.queue_declare(queue="",exclusive=True)
        self._queue = res.method.queue
        self._channel.queue_bind(queue=self._queue,
                                 exchange=self._exchange,
                                 routing_key=self._routing_key
                                 )
        return self
    



if __name__ == "__main__":
    severity = sys.argv[1]
    server = RabbitMQ("rabbit-mq","direct_logs",severity)
    server.create_connection()
    server.start_consume()

    