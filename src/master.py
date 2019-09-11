#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymodbus.client.sync import ModbusTcpClient as TcpClient
from pymodbus.client.sync import ModbusSerialClient as SerialClient
# from pymodbus.constants import Endian
# from pymodbus.payload import BinaryPayloadDecoder
# from pymodbus.payload import BinaryPayloadBuilder
# from collections import OrderedDict
import time
import numpy as np

import logging


# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)





class TCP_Client():
    ''' Obsłoga Modbus TCP'''

    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.client = TcpClient(host=self.host, port=self.port)
        self.connection = self.client.connect()


class RTU_Client():
    ''' Obsłoga Modbus RTU'''

    def __init__(self, speed, rs_port, method='rtu', stopbits=1,parity='N', bytesize=8, timeout=1,):
        self.method = method
        self.rs_port = rs_port
        self.speed = speed
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.timeout = timeout
        self.client = SerialClient(method=self.method, port=self.rs_port, baudrate=self.speed, stopbits=self.stopbits,
                                   parity=self.parity, bytesize=self.bytesize, timeout=self.timeout)
        self.connection = self.client.connect()

class Master():
    def __init__(self, device_adress, data_type, start_adress, length,client):

        self.device_adress = device_adress
        self.data_type = data_type
        self.start_adress = start_adress
        self.length = length
        self.client=client


    def assercion(self, operation, unit):
        '''
        Sprawdznie bledow w polaczeniu
            :param operation: operacja do sprawdzenia bledu
            :param unit: adres sprawdzanego urzadzenia
            :return: zwraca blad lub nie robuc nic
        '''
        # test that we are not an error
        if not operation.isError():
            pass
        else:
            print("Bład polaczenia z adresem ", unit)
        return operation.isError()

    def read_holding(self):
        '''
        Funkcja odczytu holding registerow.
        '''
        massure = self.client.read_holding_registers(self.start_adress, self.length, unit=self.device_adress)
        # sprawdzenie czy nie ma errorow
        if self.assercion(massure, self.device_adress) == False:

            return massure.registers[0:]
        else:
            return False


if __name__ == '__main__':
    staski = TCP_Client('192.168.0.35', 502)
    client = staski.client
    red=Master(1,'holding',1,10,client)
    reg = red.read_holding()
    print(reg)
    pass
