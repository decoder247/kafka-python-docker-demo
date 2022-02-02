#!/bin/bash
#
# Running docker commands instead of docker compose
# Run each in tmux!!

IMAGE_ZOOKEEPER='zookeeper:3.4.9'
IMAGE_KAFKA='confluentinc/cp-kafka:5.3.0'
IMAGE_KAFDROP='obsidiandynamics/kafdrop:3.28.0'
NETWORK_NAME='kafka-demo'

OUTPUT_FOLDER="${HOME}/psl/code-snippets/.local/kafka-demo-output"
mkdir -p $OUTPUT_FOLDER

# Create bridge network (default bridge doesn't work!)
docker network create --driver bridge ${NETWORK_NAME} # bridge is default, but specified here for explicitness

# Run zookeeper
# NOt needed for 1 node -  -> tells the network loc of zookeeper
cmd="""
docker run -it --rm \
    --env ZOO_MY_ID=1 \
    --env ZOO_PORT=2181 \
    --env ZOO_SERVERS=server.1=zookeeper:2888:3888 \
    -v ${OUTPUT_FOLDER}/data/zookeeper/data:/data \
    -v ${OUTPUT_FOLDER}/data/zookeeper/datalog:/datalog \
    --publish 2181:2181 \
    --network=${NETWORK_NAME} \
    --name zookeeper \
    --hostname zookeeper \
    ${IMAGE_ZOOKEEPER}
"""
tmux new-session -d -s zookeeper
tmux send-keys -t zookeeper "$cmd" enter

# Run kafka server (i.e. broker) after x seconds
# Likely deprecated: --env KAFKA_ADVERTISED_HOST_NAME=kafka1
# KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 -> REQUIRED!! Otherwise error bcs the default offsets_topic which stores offset info has replication = 3 by default
sleep 2
cmd="""
docker run -it --rm \
    --env KAFKA_BROKER_ID=1 \
    --env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
    --env KAFKA_ADVERTISED_LISTENERS=LISTENER_DOCKER_INTERNAL://kafka1:19091,LISTENER_DOCKER_EXTERNAL://${DOCKER_HOST_IP:-127.0.0.1}:9091 \
    --env KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=LISTENER_DOCKER_INTERNAL:PLAINTEXT,LISTENER_DOCKER_EXTERNAL:PLAINTEXT \
    --env KAFKA_INTER_BROKER_LISTENER_NAME=LISTENER_DOCKER_INTERNAL \
    --env KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    -v ${OUTPUT_FOLDER}/data/kafka1/data:/var/lib/kafka/data \
    --publish 9091:9091 \
    --network=${NETWORK_NAME} \
    --name kafka1 \
    --hostname kafka1 \
    ${IMAGE_KAFKA}
"""
tmux new-session -d -s kafka1
tmux send-keys -t kafka1 "$cmd" enter

# Run kafdrop ui
cmd="""
docker run -it --rm \
    --env KAFKA_BROKERCONNECT=kafka1:19091 \
    --publish 9000:9000 \
    --network=${NETWORK_NAME} \
    --name kafdrop \
    ${IMAGE_KAFDROP}
"""
tmux new-session -d -s kafdrop
tmux send-keys -t kafdrop "$cmd" enter


