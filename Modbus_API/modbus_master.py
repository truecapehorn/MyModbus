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

    def __init__(self, host, port):
        self.host = host
        self.port = port
        try:
            self.client = TcpClient(host=self.host, port=self.port)
            self.connection = self.client.connect()
            if self.connection == False:
                print('Brak Polaczenia')
                exit(1)

        except Exception as e:
            print(e)
            exit(1)


class RTU_Client():
    ''' Obsłoga Modbus RTU'''

    def __init__(self, speed, rs_port, method='rtu', stopbits=1, parity='N', bytesize=8, timeout=1, ):
        self.method = method
        self.rs_port = rs_port
        self.speed = speed
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.timeout = timeout

        try:
            self.client = SerialClient(method=self.method, port=self.rs_port, baudrate=self.speed,
                                       stopbits=self.stopbits,
                                       parity=self.parity, bytesize=self.bytesize, timeout=self.timeout)
            self.connection = self.client.connect()
            if self.connection == False:
                print('Brak Polaczenia')
                exit(1)
        except Exception as e:
            print(e)
            exit(1)

# ====================================================================================================================

class Master():

    def __init__(self, client):
        self.client = client

    def read_holding(self):
        self.reg_type = 'holding'


        massure = self.client.read_holding_registers(self.reg_start, self.reg_lenght, unit=self.unit)
        if self.assercion(massure) == False: # sprawdzenie czy nie ma errorow
            return massure.registers[0:]

    def read_input(self):
        self.reg_type = 'input'

        massure = self.client.read_input_registers(self.reg_start, self.reg_lenght, unit=self.unit)
        if self.assercion(massure) == False: # sprawdzenie czy nie ma errorow
            return massure.registers[0:]

    def write_single(self):
        self.reg_type = 'holding'

        massure = self.client.write_register(self.val, self.unit, unit=self.reg_add,)
        if self.assercion(massure) == False: # sprawdzenie czy nie ma errorow
            return print('Wartosc zapisana')

    def read_multiple_colis(self):
        self.reg_type = 'coil'
        massure = self.client.read_coils(self.start, self.count, unit=self.unit)
        if self.assercion(massure) == False: # sprawdzenie czy nie ma errorow
            return massure.bits[0:self.count]

# ------------------------------------------------------------------------------------------------------------------

    def assercion(self, operation):
        '''
        Sprawdznie bledow w polaczeniu
            :param operation: operacja do sprawdzenia bledu
            :return: zwraca blad lub nie robuc nic
        '''
        # test that we are not an error
        if not operation.isError():
            pass
        else:
            print("Bład polaczenia z adresem ", self.unit, 'Typ: ', self.reg_type, "\nWyjątek: ", operation)
        return operation.isError()

    def choise_data_type(self, data):
        """Jezli data bedzie typu long to trzeba zrobic rekompozycje rejestrow 16bit lub nie
            Wrzycenie do numpy i przerobienie z int 16  na float 32
        """
        if self.data_type != 'int':
            if self.transp != None:  # transpozycja tablicy [0,1] na [1,0]
                data[0::2], data[1::2] = data[1::2], data[0::2]
            data_arr = np.array([data], dtype=np.int16)
            data_as_float = data_arr.view(dtype=np.float32).tolist()[0]  # to list zmienia na liste i pomija [[]]
            data = data_as_float
        else:
            pass
        return data

    def display_data(self, data, start):
        """
        Wydrukowanie wynikow
            :param data: Odczytana tablica z rejstrami
            :param start: Startowy adres rejestru
            :return:
        """
        if len(data) > 0:
            if type(data) != bool:
                dic_val = {str(nr + start): v for nr, v in enumerate(data)}
            else:
                dic_val = data
            return_dict = {'Device': self.unit, 'Reg_type': self.reg_type, 'Data': dic_val}
        else:
            print('Brak Danych')
        return return_dict

# ---------------------------------------------------------------------------------------------------------------------

    def read_coils(self, start, count):
        self.start = start
        self.count = count

        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        measure = self.read_multiple_colis()
        self.client.close()
        dicData = self.display_data(measure, self.start)  # zamiana na slownik i wydruk
        return dicData



    def write_register(self, reg_add, val, unit):
        """
        :param reg_add_wr: Adres rejestru do zapisu
        :param val_wr: Wartosc do zapisu
        :param unit_wr: Adres urzadznia do zapisu
        :return:
        """
        self.reg_add = reg_add
        self.val = val
        self.unit = unit

        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        self.write_single()
        self.client.close()
        return print('\tNowa wartosc zapisana')

    def read_register(self, unit, reg_start, reg_lenght, reg_type='holding', data_type='int', transp=None):

        self.unit = unit
        self.reg_start = reg_start
        self.reg_lenght = reg_lenght
        self.reg_type = reg_type
        self.data_type = data_type
        self.transp = transp

        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        time.sleep(0.2)
        if self.reg_type == 'holding':
            data = self.read_holding()
        elif self.reg_type == "input":
            data = self.read_input()
        self.client.close()
        d_type = self.choise_data_type(data)  # wynik odczytu jako lista w zaleznosci od traspozycji
        dicData = self.display_data(d_type, self.reg_start)  # zamiana na slownik i wydruk
        return dicData

# ===================================================================================================================

if __name__ == '__main__':
    staski = TCP_Client('37.26.192.248', 502)
    conn = Master(staski.client)

    reg = conn.read_register(1, 101, 10, reg_type='holding')
    print(reg)

    coil = conn.read_coils(95, 10)
    print(coil)
    try:
        for k, v in coil['Data'].items():
            if v == True:
                print(k, v)
    except Exception:
        pass
