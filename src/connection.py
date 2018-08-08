#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from collections import OrderedDict
import time
import numpy as np

class Connection():
    ''' Obsłoga Modbus RTU'''

    def __init__(self, method='rtu', port='', speed=0, stopbits=1, parity='N', bytesize=8, timeout=1):
        self.method = method
        self.port = port
        self.speed = speed
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.timeout = timeout

    def connection(self):
        client = ModbusClient(method=self.method, port=self.port, baudrate=self.speed, stopbits=self.stopbits,
                              parity=self.parity, bytesize=self.bytesize, timeout=self.timeout)

    def discrabe_connection(self):
        print(
            "   Connection:\nmethod = {},\nport = {},\nbaudrate = {},\nstopbits = {},\nparity = {},\nbytesize = {},\ntimeout = {},\n".format(
                self.method,
                self.port,
                self.speed,
                self.stopbits,
                self.parity,
                self.bytesize,
                self.timeout))

        time.sleep(1)

