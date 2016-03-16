#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

from paho.mqtt.client import Client

class MqttClient(Client):
    """Mqtt Client"""

    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 1883

    msg = "0"

    def __init__(self, topic, host=DEFAULT_HOST, port=DEFAULT_PORT):
        Client.__init__(self)
        self.user_data_set({'topic': 'altie/#',})
        self.connect(host=host, port=port)
        self.on_connect = self.on__connect
        self.on_message = self.on__message
        self.loop_start()

    @staticmethod
    def on__connect(client, userdata, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(userdata['topic'])

    @staticmethod
    def on__message(client, userdata, msg):
        MqttClient.msg = msg.payload.decode()
        print(msg.topic + ": " + msg.payload.decode())


def main(args):
    mqttc = MqttClient(topic='altie/#', host='192.168.1.15')
    while True:
        mqttc.publish("test/a",mqttc.msg)
        time.sleep(3)


if __name__ == "__main__":
    sys.exit(main(sys.argv))