
## Rabbit MQ - Direct Exchange Setup

""" 
    
    docker network create -d bridge my-net-v1
    
    docker create -p 5672:5672 -p 15672:15672 --hostname rmq --name rabbit-mq -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=admin rabbitmq:3.11-management
    docker start rabbit-mq
    docker port rabbit-mq
    docker network create -b my-net-v1
    docker network connect my-net-v1 rabbit-mq

    docker build -t q-consumer .
    docker run --rm -it --network my-net-v1 --name mq-client1 q-consumer consumer.py rabbit-mq
 """
