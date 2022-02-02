from time import sleep

from kafka_utils import *

# Hardcoded
EXAMPLE_TOPICS_LIST = [f"test_topic_{i}" for i in range(2)]

# Initialise and create producer
conf = {
    "bootstrap.servers": "localhost:9091",
}
p = create_producer(conf)

# Send to topic!
for topic in EXAMPLE_TOPICS_LIST:
    send_to_topic(p, topic=topic, key="hello", value="world")
    sleep(0.05)

# p.close()
