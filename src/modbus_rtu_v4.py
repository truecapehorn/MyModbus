#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from collections import OrderedDict
import time
import numpy as np


class Master():
    ''' Obsłoga Modbus RTU'''

    def __init__(self, method='rtu', port='', speed=9600, stopbits=1, parity='N', bytesize=8, timeout=1):
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
        return client


class Registers():

    def __init__(self, client):
        self.client = client

    def reg_holding(self, unit, reg_start, reg_lenght):
        massure = self.client.read_holding_registers(reg_start, reg_lenght, unit=unit)
        return massure

    def reg_input(self, unit, reg_start, reg_lenght):
        massure = self.client.read_input_registers(reg_start, reg_lenght, unit=unit)
        return massure

    def read_holding(self):

if __name__ == '__main__':
    apar = Master(port='com2', speed=2400)
    client = apar.connection()
    print(client)
    regs = Registers(client)
    if client.connect():
        print("dups")
        print(regs)
        masure=regs.read_holding(2,0,2)
        print(masure.registers[0:])


