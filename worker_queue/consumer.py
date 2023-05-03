try:
    import pika
    import sys
    import time
except Exception as e:
    print("Some modules are missing {}".format(e))


class RabbitMQ:

    def __init__(self,host,queue) -> None:
        self.host = host
        self._queue = queue
        self._credential = pika.PlainCredentials("admin","admin")
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,
                                                                             credentials=self._credential))
        self._channel = self._connection.channel()
        self._channel.queue_declare(self._queue,durable=True)
        self._channel.basic_qos(prefetch_count=1)
    
    def callback(self,ch, method, properties, body):
        print("[x] Recieved %r " % body.decode('utf-8'))
        time.sleep(10)
        ch.basic_ack(delivery_tag = method.delivery_tag)
    
    def start_consumer(self):
        #self._channel.basic_consume(self._queue,on_message_callback=self.callback,auto_ack=True)
        self._channel.basic_consume(self._queue,on_message_callback=self.callback,auto_ack=False)
        print("[*] Starting consumer client...")
        self._channel.start_consuming()


if __name__ == "__main__":
    host = "localhost"
    if len(sys.argv)>=1:
        host = sys.argv[1]
    message_queue = RabbitMQ(host,"test-queue")
    message_queue.start_consumer()


