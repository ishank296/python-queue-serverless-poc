try:
    import pika
    import sys
except Exception as e:
    print("Some modules are missing %s " % str(e))


class Consumer:

    def __init__(self,host,exchange) -> None:
        self._host = host
        self._exchange = exchange
        self._credential = pika.PlainCredentials(username='admin',password='admin')
        self._connection = pika.BlockingConnection(
            parameters=pika.ConnectionParameters(host=host,credentials=self._credential))
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self._exchange,exchange_type="fanout")
        queue = self._channel.queue_declare(queue="",exclusive=True)
        self._queue_name = queue.method.queue
        self._channel.queue_bind(queue=self._queue_name,exchange=self._exchange)

    def callback(self,ch, method, properties, body):
        print("[*] received message %r" % body)
    
    def start_consumer(self):
        self._channel.basic_consume(queue=self._queue_name,on_message_callback=self.callback,auto_ack=True)
        print("[*] Starting consumer client...")
        self._channel.start_consuming()


if __name__ == "__main__":
    RabbitMQ = Consumer("rabbit-mq","fanout_test_1")
    RabbitMQ.start_consumer()
    