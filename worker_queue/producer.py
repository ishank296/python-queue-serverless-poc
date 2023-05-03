try:
    import pika
    import time
except Exception as e:
    print("Some modules are missing {}".format_map(e))


class RabbitMQ:

    def __init__(self, host, queue, exchange="") -> None:
        self.host = host
        self._credential = pika.PlainCredentials('admin','admin')
        self.queue = queue
        self._exchange = exchange

    def __enter__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,
                                                               credentials=self._credential))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.queue,durable=True)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._connection.close()

    def publish(self,routing_key,message={}):
        if self._exchange =="":
            routing_key = self.queue
        self._channel.basic_publish(exchange=self._exchange,
                      routing_key=routing_key,
                      body=str(message))


if __name__ == "__main__":
    payload = {
        "id":43455,
        "category":"payment",
        "amount":5483,
        "item_type":"trn_in"
    }
    #message_queue = 
    #message_queue.publish("python",message=payload)
    with RabbitMQ("localhost","test-queue","test-exchange") as queue:
        for i in range(20):
            time.sleep(3)
            print("publishing message %s" % str(payload))
            queue.publish('python',str(payload))


