#!/bin/bash
#
# Stops docker-run.sh

NETWORK_NAME='kafka-demo'
OUTPUT_FOLDER="${HOME}/psl/code-snippets/.local/kafka-demo-output"

# Stop processes (in reverse order) and remove network
# https://stackoverflow.com/questions/56939408/what-is-the-right-order-to-stop-start-kafka-with-zookeeper-and-schema-registry/56939714
docker stop kafdrop; \
    docker stop kafka1; \
    docker stop zookeeper; \
    docker network rm ${NETWORK_NAME}

# Kill tmux servers
tmux kill-session -t kafdrop && \
    tmux kill-session -t kafka1 && \
    tmux kill-session -t zookeeper

# Remove output dir
rm -r $OUTPUT_FOLDER
