from confluent_kafka.admin import AdminClient, NewTopic

from kafka_utils import *

# Hardcoded
HOSTNAME = gethostname()
EXAMPLE_TOPICS_LIST = [f"test_topic_{i}" for i in range(2)]
# ["test_topic_1","test_topic_2"]

# Set config params
conf = {
    "bootstrap.servers": "localhost:9091",
    "client.id": HOSTNAME,  # Probably unecssary
}

# Create admin object
admin_client = AdminClient(conf)

# Create newtopic and add to topic list
topic_list = [
    create_topic(EXAMPLE_TOPIC, num_partitions=1, replication_factor=1)
    for EXAMPLE_TOPIC in EXAMPLE_TOPICS_LIST
]

# Submit topic!
fs = submit_topics(admin_client, topic_list, silent=False)
