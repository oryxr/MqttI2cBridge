#! /usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import sys
import argparse
import time


import paho.mqtt.client as mqtt
from pyA20 import i2c
from stackFifoLifo import StackFifo

debug = False

mqttc = mqtt.Client()
userdata = argparse.Namespace()
stack_i2c = StackFifo()


def close_program(sig, frame):
    """Function which close clearly the program"""
    mqttc.loop_stop()
    if sig == int(signal.SIGINT):
        if debug:
            print("Shutdown with <Ctrl-c>")
    sys.exit(0)


def parse_args():
    """Function for parsing consol arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Debug option")
    grp_mqtt = parser.add_argument_group('MQTT')
    grp_mqtt.add_argument("--topic", type=str, default="i2c",
                          help="mqtt topic")
    grp_mqtt.add_argument("--host", type=str, default="localhost",
                          help="ip address of host")
    grp_mqtt.add_argument("--port", type=int, default=1883,
                          help="port of the connected borker")
    grp_i2c = parser.add_argument_group('I2C')
    grp_i2c.add_argument("--bus", type=str, default="/dev/i2c-1",
                         help="bus I2C")
    return parser.parse_args()


class DeviceNotFoundException(IOError):
    """Raised if we cannot communicate with the device."""


class I2CBusNotConfiguredProperly(IOError):
    """Raised if we can't find the propber i2cbus setup"""


class I2CBus(object):
    """Represent an I2C bus to read / write data.

    Attributes:
        address: integer, the address where mod-io can be found.
    """
    def __init__(self, bus):
        """Instantiates a I2CBus

        Args:
            bus: string, path to bus
            address: integer, generally 0x58, the address where
            mod-io can be found
        """
        try:
            i2c.init(bus)
        except IOError:
            raise I2CBusNotConfiguredProperly(
                "could not find files for access to I2C bus,"
                "you need to load the proper modules")

    def Write(self, address, payload):
        """Sends a request to olimex mod-io.

        Args:
            key: integer, an address where to wite data.
            value:
        """
        data = []
        for val in payload:
            data.append(val)
        print(data)
        try:
            i2c.open(address)
            i2c.write(data)
            i2c.close()
        except IOError:
            raise DeviceNotFoundException("Could not communicate with device")

    def ReadBlock(self, address, key, value):
        """Reads a block from olimex mod-io.

        Args:
            key: interger, an address where to read data from.
            length: integer, how much data to read.
        """
        try:
            i2c.open(address)
            i2c.write(key)
            value = i2c.read(value)
            i2c.close()
            return value
        except IOError:
            raise DeviceNotFoundException("Could not communicate with device")

    def Read(self, address, payload):
        buffer = self.ReadBlock(address, payload[0], payload[1])
        data = [0x00]*payload[1]
        for i in range(len(buffer)):
            data[i] = buffer[i]
        return data


def on_connect(client, userdata, rc):
    if debug:
        print("Connected with result code " + str(rc))
    client.subscribe(userdata.topic+"/#")


def on_message(client, userdata, msg):
    if debug:
        print(msg.topic + " : " + msg.payload.decode())
    stack_i2c.stack({'topic': msg.topic.split('/')[1:],
                     'payload': msg.payload.decode()
                     })


def main(args):
    """
    Mqtt <--> i2c Bridge
    ====================
    """
    global debug
    debug = args.debug
    i2c_bus = I2CBus(args.bus)
    userdata.topic = args.topic
    mqttc.user_data_set(userdata)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect(args.host, args.port, 60)
    mqttc.loop_start()

    while True:
        if debug:
            print(stack_i2c.copyStack())
            time.sleep(3)
        if not stack_i2c.emptyStack():
            i2c_order = stack_i2c.unstack()
            if i2c_order['topic'][0] == "write":
                i2c_bus.Write(int(i2c_order['topic'][1], 16),
                              [int(val, 16)
                               for val in i2c_order['payload'].split(" ")]
                              )
            elif i2c_order['topic'][0] == "read":
                if debug:
                    print([[int(i2c_order['payload'].split(" ")[0], 16)],
                           int(i2c_order['payload'].split(" ")[1])])
                res = i2c_bus.Read(int(i2c_order['topic'][1], 16),
                                   [[int(i2c_order['payload'].split(" ")[0],
                                         16)],
                                    int(i2c_order['payload'].split(" ")[1])]
                                   )
                print(res)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, close_program)
    sys.exit(main(parse_args()))
