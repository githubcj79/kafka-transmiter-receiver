#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decouple import config
import hashlib
import json
from kafka import KafkaConsumer
import os

KAFKA_BROKER_URL = config('KAFKA_BROKER_URL')
TRANSACTIONS_TOPIC = config('TRANSACTIONS_TOPIC')
CONSUMER = None

def receiver(topic=None):
    global CONSUMER

    if not topic:
        return None

    if not CONSUMER:
        CONSUMER = KafkaConsumer(
            TRANSACTIONS_TOPIC,
            bootstrap_servers=KAFKA_BROKER_URL,
            value_deserializer=lambda value: json.loads(value),
        )

    for message in CONSUMER:
        message = message.value
        if message['beginning']:
            # Assumes the default UTF-8 for str_.
            str_ = ""
        elif message['data']:
            str_ = str_.join(message['chunk'])
        elif message['ending']:
            hash_object = hashlib.md5(str_.encode())
            return message['hash'] == hash_object.hexdigest(), str_


if __name__ == '__main__':
    while True:
        ok, str_ = receiver(topic=TRANSACTIONS_TOPIC)
        print(f"ok[{ok}]")
        print(f"str_[{str_}]")
        print('_' * 32)
