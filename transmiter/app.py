#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decouple import config
import hashlib
import json
from kafka import KafkaProducer
import os
from time import sleep

TRANSACTIONS_TOPIC = config('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = config('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(config('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND
CHUNK_SIZE = int(config('CHUNK_SIZE'))
MAX_SIZE = int(config('MAX_SIZE'))
PRODUCER = None

# La idea: recibir un str_ grande > 1 MB
# tomarle hash
# mensaje de inicio
# enviarlo en trocitos
# mensaje de término + hash

def transmiter(topic=None,str_=None):
    '''
    Assumes the default UTF-8 for str_.
    '''
    global PRODUCER

    if not topic or not str_:
        return False

    if not PRODUCER:
        PRODUCER = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            # Encode all values as JSON
            value_serializer=lambda value: json.dumps(value).encode(),
        )

    # enviar msg de inicio
    message = {
                'beginning': True,
                'ending': False,
                'data':False
    }
    PRODUCER.send(topic,value=message)

    # tomar hash
    hash_object = hashlib.md5(str_.encode())
    print(f"hexdigest[{hash_object.hexdigest()}]")

    # trozar el mensaje
    n = CHUNK_SIZE
    print(f"str_[{str_}]")
    for i in range(0, len(str_), n):
        chunk = str_[i:i+n]
        message = {
                    'beginning': False,
                    'ending': False,
                    'data':True,
                    'chunk':chunk
        }
        PRODUCER.send(topic,value=message)
        sleep(SLEEP_TIME)

    # enviar msg de término + hash
    message = {
                'beginning': False,
                'ending': True,
                'data':False,
                'hash':hash_object.hexdigest()
    }
    PRODUCER.send(topic,value=message)

    return True


if __name__ == '__main__':
    from random import choices
    from string import ascii_letters, digits

    account_chars = digits + ascii_letters

    while True:
        str_ = ''.join(choices(account_chars, k=MAX_SIZE))
        # print(f"str_[{str_}]")
        ok = transmiter(topic=TRANSACTIONS_TOPIC,str_=str_)
        print(f"ok[{ok}]")
