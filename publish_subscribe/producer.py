try:
    import sys
    import time
    import pika
except Exception as e:
    print("Some modules are missing %s" % str(e))


class Producer:

    def __init__(self,host,exchange) -> None:
        self._host = host
        self._exchange = exchange
        self._credential = pika.PlainCredentials(username='admin',
                                                 password='admin')

    def publish(self,payload):
        self._channel.basic_publish(exchange=self._exchange,routing_key="",body=payload)

    def __enter__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host,
                                                                             credentials=self._credential))
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self._exchange,exchange_type="fanout")
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._connection.close()



if __name__ == "__main__":
    RabbitMQ = Producer("localhost","fanout_test_1")
    with RabbitMQ as queue:
        for i in range(20):
            print(f"sending message id {i}")
            time.sleep(3)
            queue.publish(f"This is test payload {i}")

