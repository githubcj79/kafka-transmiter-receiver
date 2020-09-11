#!/bin/sh

docker exec -t kafka-docker_kafka_1 kafka-topics.sh --bootstrap-server :9092 \
--create --topic queueing.transactions --partitions 1 --replication-factor 1

docker exec -t kafka-docker_kafka_1 kafka-topics.sh --bootstrap-server :9092 --describe --topic queueing.transactions

docker exec -t kafka-docker_kafka_1 kafka-topics.sh --bootstrap-server :9092 --list
