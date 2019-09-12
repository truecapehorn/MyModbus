﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from collections import OrderedDict
import time
import numpy as np
import logging



# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)


class RTU_Master():
    ''' Obsłoga Modbus RTU'''

    def __init__(self, speed, port, method='rtu', stopbits=1, parity='N', bytesize=8, timeout=1):
        self.method = method
        self.port = port
        self.speed = speed
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.timeout = timeout
        self.client = ModbusClient(method=self.method, port=self.port, baudrate=self.speed, stopbits=self.stopbits,
                                   parity=self.parity, bytesize=self.bytesize, timeout=self.timeout)
        self.connection = self.client.connect()

    def masterDoc(self):

        conn = {"connection": self.connection, "method": self.method, "port": self.port, "baudrate": self.speed,
                "stopbits": self.stopbits, "parity": self.parity, "bytesize": self.bytesize,
                "timeout": self.timeout, }
        return print("Parametry: ", conn)

    def read_register(self, unit, reg_start, reg_lenght, reg_type='holding', data_type='int'):

        '''

        :param unit: adres urzadzenia
        :param reg_start: rejestr poczatkowy
        :param reg_lenght: dlugosc rejestru
        :param reg_type: typ rejestru czy (holding lub input) def. holding
        :param data_type: int czy float
        :return: zwraca odzcytane rejestry
        '''

        """Funkcja glowna odczytu rejestrow, wywolujaca inne podfunkcje"""

        parm = [unit, reg_start, reg_lenght]
        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        time.sleep(0.2)
        if reg_type == 'holding':
            data = self.read_holding(parm)
        elif reg_type == "input":
            data = self.read_input(parm)
        self.client.close()
        measure = self.choise_data_type(data, data_type)
        self.display_data(measure, unit, reg_start)
        return measure

    def write_register(self, reg_add, val, unit):
        '''

        :param reg_add: adres rejestru do zmiany
        :param val: nowa wratosc rejstru
        :param unit: adres urzadzenia w ktorej chcemy zmienic rejstr
        :return: zwaraca zmiane rejstru
        '''
        parm = [unit, reg_add, val]
        self.write_single_register(parm)
        self.client.close()
        return print('\tNowa wartosc zapisana')

    def read_holding(self, parm):
        '''

        :param parm: tablica z ( unit, reg_start, reg_lenght )
        :return: laczy sie z clientem i odczytuje holding reg. Sprawdza czy sa blady w polaczeniu
        Jezli sa to funckcja assertion zwraca blad polaczenia.
        '''
        massure = self.client.read_holding_registers(parm[1], parm[2], unit=parm[0])
        # sprawdzenie czy nie ma errorow
        if self.assercion(massure, parm[0]) == False:

            return massure.registers[0:]
        else:
            return False

    def read_input(self, parm):
        '''

        :param parm: tablica z ( unit, reg_start, reg_lenght )
        :return: laczy sie z clientem i odczytuje input reg. Sprawdza czy sa blady w polaczeniu
        Jezli sa to funckcja assertion zwraca blad polaczenia.
        '''
        massure = self.client.read_input_registers(parm[1], parm[2], unit=parm[0])
        if self.assercion(massure, parm[0]) == False:

            return massure.registers[0:]
        else:
            return False

    def write_single_register(self, parm):
        self.client.write_register(parm[1], parm[2], unit=parm[0])

    def assercion(self, operation, unit):
        '''

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

    def check_write(self, parm):
        pass

    def choise_data_type(self, data, data_type):
        """Jezli data bedzie typu long to trzeba zrobic rekompozycje rejestrow 16bit"""
        if data_type != 'int':
            data[0::2], data[1::2] = data[1::2], data[0::2]
            data_arr = np.array([data], dtype=np.int16)
            data_as_float = data_arr.view(dtype=np.float32)
            data = data_as_float
        else:
            pass
        return data

    def display_data(self, data, unit, reg_start):
        dic_val = {}
        if data != False:
            for nr, v in enumerate(data):
                dic_val[nr + reg_start] = v
            print("Urzadzenie {} - {}".format(str(unit), dic_val))
        else:
            pass


# TODO: Dziala odczyt i zapis single reg.
# TODO: Zrobic program glowny
# TODO: Zmienic na klasy


if __name__ == '__main__':

    pass