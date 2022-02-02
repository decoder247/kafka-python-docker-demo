import json
from sys import stderr
from time import sleep

from confluent_kafka import Consumer, KafkaError, KafkaException

from kafka_utils import *

# https://stackoverflow.com/questions/43045590/kafka-setup-with-docker-compose
# https://rmoff.net/2018/08/02/kafka-listeners-explained/
# https://stackoverflow.com/questions/53247553/kafka-access-inside-and-outside-docker

# Hardcoded
EXAMPLE_TOPICS_LIST = [f"test_topic_{i}" for i in range(2)]
MIN_COMMIT_COUNT = 3
RUNNING = True
POLL_TIMEOUT = 1


def print_assignment(consumer, partitions):
    print("Assignment:", partitions)


# Create and initialise consumer, belonging to consumer group
conf = {
    "bootstrap.servers": "localhost:9091",
    "group.id": "example-group2",
    "client.id": "client-1",  # optional identifier of a Kafka consumer
    "auto.offset.reset": "earliest",
    # "session.timeout.ms": 6000,
    # "enable.auto.commit": True,
    # "default.topic.config": {"auto.offset.reset": "smallest"},
}
consumer = Consumer(conf)

# Define what to do with message
def msg_process(msg):
    # Print full message
    print(msg)
    print(msg.value())
    # stderr.write(f"{msg.topic()} [{msg.partition()}] at offset {msg.offset()} with key {str(msg.key())}:\n")
    sleep(0.1)


# Main loop (synchronous)
# For async via polling, see - https://docs.confluent.io/clients-confluent-kafka-python/current/overview.html#python-demo-code
try:
    # Subscribe to topics
    print("subscribing...")
    consumer.subscribe(
        EXAMPLE_TOPICS_LIST  # , on_assign=print_assignment, on_revoke=print_assignment
    )

    msg_count = 0
    while RUNNING:
        # Query topics
        msg = consumer.poll(timeout=POLL_TIMEOUT)

        # Not received
        if msg is None:
            print(f"OK: poll() timeout after {POLL_TIMEOUT}s")
            continue

        # Process message otherwise
        elif not msg.error():
            msg_process(msg)
            msg_count += 1
            print(msg_count)

        # Check error - End of partition event or otherwise
        elif msg.error().code() == KafkaError._PARTITION_EOF:
            print(
                f"% {msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}\n"
            )
        else:
            raise KafkaException(msg.error())

except KeyboardInterrupt:
    stderr.write("%% Aborted by user\n")

finally:
    # Close down consumer to commit final offsets.
    consumer.close()
