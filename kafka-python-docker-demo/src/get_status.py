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
admin_client = create_admin_client(conf)

# List topics
print(f"Topics list:\n{get_topics(admin_client)}\n")

# List groups
print(f"Groups list:\n{get_groups(admin_client)}\n")
