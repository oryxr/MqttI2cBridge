#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import MqttI2cBridge

setup(
    name='MqttI2cBridge',
    version=MqttI2cBridge.__version__,
    packages=find_packages(),
    author="Pierre Lucas",
    author_email="pierre.lucas@altie.fr",
    description="Bridge between i2c and MQTT",
    long_description=open('README.md').read(),
    # install_requires = ,  # dependancies (type list: ["gunicorn","docutils
    # >=0.3"])
    include_package_data=True,  # use MANIFEST.in
    url = 'http://github.com/oryxr/MqttI2cBridge',  # official page of librarie
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Communications",
    ],
    license= "GPL",
)