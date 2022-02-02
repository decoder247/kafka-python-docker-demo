#!/bin/bash
#
# Insert description

# Pull main images
IMAGE_ZOOKEEPER=zookeeper           # Small image and official
IMAGE_KAFKA=wurstmeister/kafka      # 
docker pull ${IMAGE_ZOOKEEPER}
docker pull ${IMAGE_KAFKA}

# Run zookeeper with port 2181
docker run -it --rm \
    -p 2181:2181 \
    --name zookeeper \
    ${IMAGE_ZOOKEEPER}

# Run kafka with port 9092
docker run -it --rm \
    -p 9092:9092 \
    -e KAFKA_ZOOKEEPER_CONNECT=iliono:2181 \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://iliono:9092 \
    -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    --name kafka \
    ${IMAGE_KAFKA}
