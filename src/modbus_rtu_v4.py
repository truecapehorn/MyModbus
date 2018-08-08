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



        print(
            "   Connection:\nmethod = {},\nport = {},\nbaudrate = {},\nstopbits = {},\nparity = {},\nbytesize = {},\ntimeout = {},\n".format(
                self.method,
                self.port,
                self.speed,
                self.stopbits,
                self.parity,
                self.bytesize,
                self.timeout))

    def connection(self):
        client = ModbusClient(method=self.method, port=self.port, baudrate=self.speed, stopbits=self.stopbits,
                              parity=self.parity, bytesize=self.bytesize, timeout=self.timeout)

        return client

    def reg_holding(self, client, parm):
        massure = client.read_holding_registers(parm[1], parm[2], unit=parm[0])
        return massure.registers[0:]

    def reg_input(self, client, parm):

        massure = client.read_input_registers(parm[1], parm[2], unit=parm[0])
        return massure.registers[0:]

    def choise_data(self,data,data_type):
        if data_type != 'int':
            data[0::2], data[1::2] = data[1::2], data[0::2]
            data_arr = np.array([data], dtype=np.int16)
            data_as_float = data_arr.view(dtype=np.float32)
            data = data_as_float
        else:
            pass
        return data

    def display_data(self,data):
        print(data)




    def read_register(self, unit, reg_start, reg_lenght, reg_type='holding', data_type='int'):
        client = self.connection()
        parm = [unit, reg_start, reg_lenght]
        try:
            client.connect()
            if reg_type == 'holding':
                data = self.reg_holding(client, parm)
            elif reg_type == "input":
                data = self.reg_input(client, parm)
            client.close()
            measure=self.choise_data(data,data_type)
            self.display_data(measure)
            return print('pomiar OK!!')
        except AttributeError:
            print('Połaczenie z adresem {} nie udane'.format(parm[0]))
            client.close()
        except KeyboardInterrupt:
            print('Przerwanie przez urzytkownika')
            client.close()


if __name__ == '__main__':
    apar = Master(port='com2', speed=2400)

    while True:
        apar.read_register(2, 0, 10)
        time.sleep(2)
