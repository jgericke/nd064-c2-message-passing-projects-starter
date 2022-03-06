from kafka import KafkaConsumer


TOPIC_NAME = "connections"

consumer = KafkaConsumer(TOPIC_NAME)
for message in consumer:
    print(message)
