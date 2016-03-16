#! /usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
from I2CBus import I2CBus


def error(*objs):
    print("Error: ", *objs, file=sys.stderr)


class I2cMqttBridge(object):
    """Bridge Mqtt <-> i2c"""

    def __init__(self, topic, bus):
        self._topic = topic
        self._bus = bus