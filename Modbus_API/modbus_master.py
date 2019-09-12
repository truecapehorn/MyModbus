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

        self.client = TcpClient(host=self.host, port=self.port)
        self.connection = self.client.connect()
        if self.connection == False:
            print('Brak Polaczenia z adresem {}:{}'.format(self.host, self.port))


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
        if self.assercion(massure) == False:  # sprawdzenie czy nie ma errorow
            return massure.registers[0:]

    def read_input(self):
        self.reg_type = 'input'
        massure = self.client.read_input_registers(self.reg_start, self.reg_lenght, unit=self.unit)
        if self.assercion(massure) == False:  # sprawdzenie czy nie ma errorow
            return massure.registers[0:]

    def write_single(self):
        self.reg_type = 'holding'
        massure = self.client.write_register(self.val, self.unit, unit=self.reg_add, )
        if self.assercion(massure) == False:  # sprawdzenie czy nie ma errorow
            return print('Wartosc zapisana')

    def read_multiple_colis(self):
        self.reg_type = 'coil'
        massure = self.client.read_coils(self.reg_start, self.reg_lenght, unit=self.unit)
        if self.assercion(massure) == False:  # sprawdzenie czy nie ma errorow
            return massure.bits[0:self.reg_lenght]

    def read_multipe_discrete_inputs(self):
        self.reg_type = 'input'
        massure = self.client.read_discrete_inputs(self.reg_start, self.reg_lenght, unit=self.unit)
        assertion_check = self.assercion(massure)
        if assertion_check == False:  # sprawdzenie czy nie ma errorow
            return massure.bits[0:self.reg_lenght]
        else:
            return False

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
            # print("Bład polaczenia z adresem ", self.unit, 'Typ: ', self.reg_type, "Wyjątek: ", operation)
            print("Blad polacznia z portem: {}; Typ rejstru: {}; Wyjątek: {}".format(self.client.port,
                                                                                     self.reg_type,
                                                                                     operation, ))
        return operation.isError()

    def data_check(self, data):
        try:
            iter(data)  # sprawdznie czy obiekt jest iterowalny
            return True
        except TypeError as te:
            # print('Brak Odczytanych danych')
            return False

    def choise_data_type(self, data):
        """Jezli data bedzie typu long to trzeba zrobic rekompozycje rejestrow 16bit lub nie
            Wrzycenie do numpy i przerobienie z int 16  na float 32
        """
        if self.data_type != 'int':
            if self.transp != False:  # transpozycja tablicy [0,1] na [1,0]
                data[0::2], data[1::2] = data[1::2], data[0::2]
            if self.data_type == 'float':
                data_arr = np.array([data], dtype=np.int16)
                data_as_float = data_arr.view(dtype=np.float32).tolist()[0]  # to list zmienia na liste i pomija [[]]
                data = data_as_float
            if self.data_type == 'int32':
                data_arr = np.array([data], dtype=np.int16)
                data_as_int32 = data_arr.view(dtype=np.int32).tolist()[0]  # to list zmienia na liste i pomija [[]]
                data = data_as_int32

        else:
            pass

        return data

    def display_data(self, data):
        """
        Wydrukowanie wynikow
            :param data: Odczytana tablica z rejstrami
            :param start: Startowy adres rejestru
            :return:
        """
        if self.data_type == 'int':
            dic_val = {str(nr + self.reg_start): v for nr, v in enumerate(data)}
        else:
            dic_val = {str(nr * 2 + self.reg_start): v for nr, v in enumerate(data)}  # 0,2,4,6
        return_dict = {'Device': self.unit, 'Reg_type': self.reg_type, 'Data_type': self.data_type, 'Data': dic_val}
        return return_dict

    # ---------------------------------------------------------------------------------------------------------------------

    def read_bool(self, unit, reg_start, reg_lenght, reg_type='coil'):
        self.unit = unit
        self.reg_start = reg_start
        self.reg_lenght = reg_lenght
        self.reg_type = reg_type
        self.data_type = 'bool'

        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        if self.reg_type == 'coil':
            measure = self.read_multiple_colis()
        elif self.reg_type == 'input':
            measure = self.read_multipe_discrete_inputs()
        else:
            print("Zly typ rejstru")
        self.client.close()
        if measure != False:
            data_ok = self.data_check(measure)
            if data_ok:
                dicData = self.display_data(measure)  # zamiana na slownik i wydruk
                return dicData
        else:
            pass

    def write_register(self, reg_add, val, unit):
        self.reg_add = reg_add
        self.val = val
        self.unit = unit

        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        self.write_single()
        self.client.close()
        return print('\tNowa wartosc zapisana')

    def read_register(self, unit, reg_start, reg_lenght, reg_type='holding', data_type='int', transp=False):
        self.unit = unit
        self.reg_start = reg_start
        self.reg_lenght = reg_lenght
        self.reg_type = reg_type
        self.data_type = data_type
        self.transp = transp
        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        time.sleep(0.0)
        if self.reg_type == 'holding':
            data = self.read_holding()
        elif self.reg_type == "input":
            data = self.read_input()
        self.client.close()
        if data != False:
            data_ok = self.data_check(data)
            if data_ok:
                d_type = self.choise_data_type(data)  # wynik odczytu jako lista w zaleznosci od traspozycji
                dicData = self.display_data(d_type)  # zamiana na slownik i wydruk
                return dicData


# ===================================================================================================================

if __name__ == '__main__':

    staski = TCP_Client('37.26.192.248', 502)
    print(staski.client.host)
    print(staski.client.timeout)

    rtu_com = RTU_Client(9600, 'com6')
    print(rtu_com.client.port)

    conn = Master(staski.client)
    try:
        reg = conn.read_register(1, 101, 10, reg_type='holding')
        print(reg)
    except Exception as e:
        print(e)

    staski = TCP_Client('37.26.192.248', 502)
    conn = Master(staski.client)
    try:
        coil = conn.read_bool(1, 1, 5, reg_type='coil')
        print(coil)
        discrete_in = conn.read_bool(1, 1, 5, reg_type='input')
        print(discrete_in)
    except Exception as e:
        print(e)
        pass

    try:
        for k, v in coil['Data'].items():
            if v == True:
                print(k, v)
    except Exception:
        pass

    sma = TCP_Client('192.168.0.240', 502)
    sma_conn = Master(sma.client)
    try:
        reg_for_check = [30201, 30233, 30531, 30775, 30795, 30803, 30805, 30813, 30837, 30839, 30769, 30771, 30773,
                         30957, 30959, 30961, 30537, 30953, 40212, 40915]
        for i in reg_for_check:
            reg_sma = sma_conn.read_register(3, i, 2, reg_type='holding', data_type='int32', transp=True)
            print(reg_sma)
    except Exception as e:
        print(e)

    cofowent = TCP_Client('192.168.0.30', 502)
    cofowent_conn = Master(cofowent.client)
    reg_cofowent = cofowent_conn.read_register(5, 0, 10, reg_type='holding', data_type='int')
    print(reg_cofowent)

