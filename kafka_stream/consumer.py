from confluent_kafka import Consumer, KafkaException, KafkaError
import json

conf = {
    'bootstrap.servers': 'localhost:19092',
    'group.id': 'my_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(**conf)
consumer.subscribe(['flights'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'.format(msg.topic(), msg.partition()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            record_value = json.loads(msg.value().decode('utf-8'))
            print(f'Consumed record value {record_value}')
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
