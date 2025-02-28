#!/usr/bin/env bash

LOG_FILE=logs/consumer.log

# Run the consumer
bin/spark-submit \
    --master spark://spark-master:7077 \
    apps/consumer.py > "${LOG_FILE}"
