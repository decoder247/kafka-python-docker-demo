from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
from socket import gethostname as ghn

"""
Example methods!! - https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/adminapi.py#L31-L48

Why need to wait when submitting topics:
- Need to wait for operation to finish  (https://github.com/confluentinc/confluent-kafka-python/issues/549)
"""


def gethostname():
    return ghn()


def get_topics(
    a: AdminClient,
) -> dict:
    return a.list_topics().topics


# More on getting groups / consumer info
# https://stackoverflow.com/questions/68933348/python-confluent-kafka-list-all-consumer-currently-listening-to-a-topic
def get_groups(
    a: AdminClient,
) -> dict:
    return a.list_groups()


def create_admin_client(
    conf: dict,
):
    return AdminClient(conf)


def create_producer(
    conf: dict,
):
    return Producer(conf)


def create_topic(
    topic: str,
    num_partitions: int = 1,
    replication_factor: int = 1,
):
    return NewTopic(
        topic=topic,
        num_partitions=num_partitions,
        replication_factor=replication_factor,
    )


def submit_topics(
    a: AdminClient,
    topic_list: list,
    silent: bool = False,
):
    """Create topics"""

    # Call create_topics to asynchronously create topics, a dict
    # of <topic,future> is returned.
    fs = a.create_topics(new_topics=topic_list)  # use validate_only=False?

    # Wait for operation to finish.
    # Timeouts are preferably controlled by passing request_timeout=15.0
    # to the create_topics() call.
    # All futures will finish at the same time.
    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None -> Some blocking present
            if not silent:
                print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))

    return fs


# Adding callback to future
# https://stackoverflow.com/questions/46388116/how-to-add-a-failure-callback-for-kafka-python-kafka-kafkaproducersend
# https://github.com/confluentinc/confluent-kafka-python/issues/487
def send_to_topic(
    p,
    topic: str,
    key: str,
    value: str,
    flush: float = 10,
):
    """
    float -> maximum time to block, for all msgs in producer queue to be delivered (before it times out)
    """
    fs = p.produce(topic=topic, key=key, value=value)
    p.flush(flush)

    return fs
