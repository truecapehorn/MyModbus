#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
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


class TCP_Master():
    ''' Obsłoga Modbus TCP'''

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = ModbusClient(host, port)
        self.connection = self.client.connect()

    def masterDoc(self):

        conn = {"connection": self.connection, "host": self.host, "port": self.port}
        return print("Parametry: ", conn)

    def read_register(self, unit, reg_start, reg_lenght, reg_type='holding', data_type='int', transp=None):

        '''
        Funkcja glowna do czytania rejestrow.

            :param unit: adres adres urzadzenia
            :param reg_start: rejestr poczatkowy
            :param reg_lenght: dlugosc rejestru
            :param reg_type: typ rejestru czy (holding lub input) def. holding
            :param data_type: int czy float
            :param transp: czy transpozycja tablucy pomiaru . big edian na litle edian czy jakos tak
            :return: zwraca odzcytane rejestry
                    [0] - słownik
                    [1] - lista
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
        measure = self.choise_data_type(data, data_type, transp)  # wynik odczytu jako lista
        dicData = self.display_data(measure, unit, reg_start)  # zamiana na slownik i wydruk
        return dicData, measure

    def write_register(self, reg_add, val, unit):
        '''
        Funkcja do zapisywania wartosci w rejestrze
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
        Funkcja odczytu holding registerow.
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
        Odczyt input registerow
            :param parm: tablica z ( unit, reg_start, reg_lenght )
            :return: laczy sie z clientem i odczytuje input reg. Sprawdza czy sa blady w polaczeniu
                Jezli sa to funckcja assertion zwraca blad polaczenia.
        '''
        massure = self.client.read_input_registers(parm[1], parm[2], unit=parm[0])
        if self.assercion(massure, parm[0]) == False:

            return massure.registers[0:]
        else:
            return False

    def read_coils(self, start, count, unit):

        massure = self.client.read_coils(start, count, unit=unit)
        return massure.bits[0:]

    def write_single_register(self, parm):
        self.client.write_register(parm[1], parm[2], unit=parm[0])

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

    def check_write(self, parm):
        pass

    def choise_data_type(self, data, data_type, transp):
        """Jezli data bedzie typu long to trzeba zrobic rekompozycje rejestrow 16bit lub nie
            Wrzycenie do numpy i przerobienie z int 16  na float 32
        """
        if data_type != 'int' and data!=False:
            if transp != None:  # transpozycja tablicy [0,1] na [1,0]
                data[0::2], data[1::2] = data[1::2], data[0::2]
            data_arr = np.array([data], dtype=np.int16)
            data_as_float = data_arr.view(dtype=np.float32).tolist()[0]  # to list zmienia na liste i pomija [[]]
            data = data_as_float
        else:
            pass
        return data

    def display_data(self, data, unit, reg_start):
<<<<<<< HEAD:src/modbus_tcp_v1.py
        dic_val=None
        if data != False:
            dic_val = {nr + reg_start: v for nr, v in enumerate(data)}
=======
        """
        Wydrukowanie wynikow
            :param data: Odczytana tablica z rejstrami
            :param unit: Adres urzadznia
            :param reg_start: Startoey adres rejestru
            :return:
        """
        if data != []:
            if type(data) != bool:
                dic_val = {nr + reg_start: v for nr, v in enumerate(data)}
            else:
                dic_val = data
>>>>>>> developerka:src/modbus_tcp.py
            print("Urzadzenie {} - {}".format(str(unit), dic_val))
        else:
            pass
        return dic_val


if __name__ == '__main__':
    staski = TCP_Master('192.168.0.35', 502)
    staski.read_register(1, 0, 120)
