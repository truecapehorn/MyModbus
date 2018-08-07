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

    def __init__(self, method='rtu', port='', speed=0, stopbits=1, parity='N', bytesize=8, timeout=1):
        self.method = method
        self.port = port
        self.speed = speed
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.timeout = timeout

    def client(self):
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


    def connection_is_true(self):
        client=self.client()
        connection=client.connect()
        print("Połącznie",connection)
        return connection


class Registers():

    def __init__(self,client):
        self.client=client


    def read_holding(self,unit,reg_start,reg_lenght):
        massure = self.client.read_holding_registers(reg_start, reg_lenght, unit=unit)
        return massure


    def read_input(self,unit,reg_start,reg_lenght):
        massure = self.client.read_input_registers(reg_start, reg_lenght, unit=unit)
        return massure




if __name__=="main":

    apar=Master(port='com3',speed=2400)
    client=apar.client()

    reg=Registers(client)

    massure=reg.read_holding(2,0,10)







