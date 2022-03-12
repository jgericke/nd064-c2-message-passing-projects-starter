import sys
import logging
from os import environ
from json import loads
from kafka import KafkaConsumer

"""Initialize logger."""
try:
    if "CONNECTIONS_CONSUMER_LOGLEVEL" in environ:
        logging.basicConfig(
            stream=sys.stdout,
            level=environ.get("CONNECTIONS_CONSUMER_LOGLEVEL"),
            format="%(asctime)s %(name)s %(levelname)s" + " %(message)s ",
        )
    else:
        logging.basicConfig(
            stream=sys.stdout,
            level="INFO",
            format="%(asctime)s %(name)s %(levelname)s" + " %(message)s ",
        )
    logger = logging.getLogger(__name__)
except (KeyError, ValueError, AttributeError, Exception):
    raise


def connections_consumer_init() -> KafkaConsumer:
    try:
        connections_consumer = KafkaConsumer(
            environ.get("KAFKA_TOPIC"),
            bootstrap_servers=[environ.get("KAFKA_URI")],
            value_deserializer=lambda x: loads(x.decode("utf-8")),
        )
        return connections_consumer
    except (KeyError, ValueError, AttributeError, Exception):
        raise


if __name__ == "__main__":

    logger.info("Starting Connections Consumer")

    connections_consumer = connections_consumer_init()
    try:
        for connection in connections_consumer:
            logger.info(f"{connection}")
    except KeyboardInterrupt:
        exit(0)
