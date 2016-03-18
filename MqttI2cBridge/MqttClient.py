#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

from paho.mqtt.client import Client

from stackFifoLifo import StackFifo


class MqttClient(Client):
    """Mqtt Client"""

    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 1883

    msg = "0"
    stackFifo = StackFifo()

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
        MqttClient.stackFifo = {'topic': msg.topic.split('/')[1:], 'payload': msg.payload.decode()}
        # MqttClient.msg = msg.payload.decode()
        print(msg.topic + ": " + msg.payload.decode())

    def read_msg(self):
        if self.stackFifo.emptyStack():
            return None
        return self.stackFifo.unstack()


def error(*objs):
    print("Error: ", *objs, file=sys.stderr)


def main(args):
    """
    MqttClient class based on paho-mqtt
    ===================================

    :Args1: <str> address ip to the broker
    :Args2: <str> topic"""
    if len(args) < 3:
        error("Need to specify a command.\n",main.__doc__)
        return 1
    mqttc = MqttClient(topic=args[2], host=args[1])
    while True:
        mqttc.publish("test/a",mqttc.msg)
        time.sleep(3)


if __name__ == "__main__":
    sys.exit(main(sys.argv))