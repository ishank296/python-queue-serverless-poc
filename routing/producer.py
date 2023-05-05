from typing import Any
import pika
import random
import time

class RabbitMQ:

    def __init__(self,host,exchange) -> None:
        self._host = host
        self._exchange = exchange
        self._credential = pika.PlainCredentials("admin","admin")
    
    def __enter__(self):
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._host,
                                    credentials=self._credential)
                                    )
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self._exchange,exchange_type="direct")
        return self
    
    
    def __exit__(self,exc_type,exc_value,exc_traceback):
        self._channel.close()
        self._connection.close()
    

    def publish(self,routing_key,payload):
        self._channel.basic_publish(exchange=self._exchange,
                                    routing_key=routing_key,
                                    body=payload)
        print(" [x] Sent %r:%r" % (routing_key, payload))


if __name__ == "__main__":
    server = RabbitMQ("localhost","direct_logs")
    severities = ["info","error","warning"]
    with server as ser:
        for i in range(20):
            severity = random.choice(severities)
            ser.publish(severity,f"[{severity}] - log test message - /101")
            time.sleep(4)
        


