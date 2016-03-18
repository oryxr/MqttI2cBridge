#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Utility functions and classes to use i2c from OlinuXino-A20-Micro.

SETUP
=====

Before using this code, you need to make sure mod-io is configured and working
on your system. Assuming you have a debian based system (like ubuntu or
raspbian):

1) edit /etc/modules, by running 'sudo -s' and opening the file with your
   favourite editor. Make sure it has the lines:

     # ... random comments ...
     i2c-dev
     i2c_bcm2708 baudrate=50000

2) once /etc/modules has been edited, run:

     $ sudo service kmod start

   to load all the modules. Alternatively, you can reboot your system.

3) make sure debugging tools and libraries are installed:

     $ sudo apt-get install i2c-tools python-smbus

3) verify that mod-io is accessible, and to which bus it is
   connected. You need to run

     $ sudo i2cdetect -y X

   with X being 0 or 1. X is the bus number. If you see a 58 (assuming you did
   not change the default address of mod-io) in the output, you found the right
   bus. Remember this number for later!

   If you don't see 58 anywhere, do you see some other number? Did you change
   mod-io address or firmware? Is it plugged correctly?  Is there a flashing
   orange led? If not, you may have problems with the firmware, power supply or
   connection of mod-io.

   Example:

   Check status of bus 0. There are all dashesh, mod-io is not here.

     $ sudo i2cdetect -y 0

            0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
       00:          -- -- -- -- -- -- -- -- -- -- -- -- --
       10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
       20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
       30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
       40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
       50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
       60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
       70: -- -- -- -- -- -- -- --

   Check status of bus 1. You can see mod-io on address 58! Good!

     $ sudo i2cdetect -y 1

            0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
       00:          -- -- -- -- -- -- -- -- -- -- -- -- --
       10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
       20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
       30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
       40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
       50: -- -- -- -- -- -- -- -- 58 -- -- -- -- -- -- --
       60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
       70: -- -- -- -- -- -- -- --

EXAMPLE
=======

"""

try:
    from pyA20 import i2c
except ImportError:
    raise ImportError("'pyA20' not install")


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

    def ReadBlock(self, address, payload):
        """Reads a block from olimex mod-io.

        Args:
            key: interger, an address where to read data from.
            length: integer, how much data to read.
        """
        try:
            i2c.open(address)
            i2c.write(payload[0])
            value = i2c.read(payload[1])
            i2c.close()
            return value
        except IOError:
            raise DeviceNotFoundException("Could not communicate with device")

