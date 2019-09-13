#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymodbus.client.sync import ModbusTcpClient as TcpClient
from pymodbus.client.sync import ModbusSerialClient as SerialClient
import time
import numpy as np

# import logging
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

    # metody cient
    def _read_holding(self):
        '''
        Funkcja pomocnicza
        :return:holding reg
        '''
        self.reg_type = 'holding'
        massure = self.client.read_holding_registers(self.reg_start, self.reg_lenght, unit=self.unit)
        if self._assercion(massure) == False:  # sprawdzenie czy nie ma errorow
            return massure.registers[0:]

    def _read_input(self):
        '''
        Funkcja pomocnicza
        :return:
        '''
        self.reg_type = 'input'
        massure = self.client.read_input_registers(self.reg_start, self.reg_lenght, unit=self.unit)
        if self._assercion(massure) == False:  # sprawdzenie czy nie ma errorow
            return massure.registers[0:]

    def _write_single(self):
        '''
        Funkcja pomocnicza
        :return:
        '''
        self.reg_type = 'holding'
        massure = self.client.write_register(self.reg_add, self.new_val, unit=self.unit)
        if self._assercion(massure) == False:  # sprawdzenie czy nie ma errorow
            return print('Wartosc zapisana')

    def _read_multiple_colis(self):
        '''
        Funkcja pomocnicza
        :return:
        '''
        self.reg_type = 'coil'
        massure = self.client.read_coils(self.reg_start, self.reg_lenght, unit=self.unit)
        if self._assercion(massure) == False:  # sprawdzenie czy nie ma errorow
            return massure.bits[0:self.reg_lenght]

    def _read_multipe_discrete_inputs(self):
        '''
        Funkcja pomocnicza
        :return:
        '''
        self.reg_type = 'disc_input'
        massure = self.client.read_discrete_inputs(self.reg_start, self.reg_lenght, unit=self.unit)
        assertion_check = self._assercion(massure)
        if assertion_check == False:  # sprawdzenie czy nie ma errorow
            return massure.bits[0:self.reg_lenght]
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    # metody pomocnicze
    def _assercion(self, operation):
        '''

        :param operation: Metoda klienta. Sprawdza czy sciagnelo dane.
        :return: Status False to OK or True to chujowo.
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

    def _data_check(self, data):
        '''
        Sprawdza czy obiekt jest iterowalny.
        :param data: Pobrana lista rejestrow.
        :return: True to OK ,False to chujowo.
        '''
        try:
            iter(data)  # sprawdznie czy obiekt jest iterowalny
            return True
        except TypeError as te:
            # print('Brak Odczytanych danych')
            return False

    def _choise_data_type(self, data):
        '''
        Sprawdza czy trzeba zamienic miejscami rejstry i koduje do opowiedniego formatu.
        :param data: Pobrana lista rejestrow
        :return: Lista w formacie danych jaki jest potrzebny. int, int32 lub float.
        '''
        if self.data_type != 'int':
            if self.transp != False:  # transpozycja tablicy [0,1] na [1,0]
                data[0::2], data[1::2] = data[1::2], data[0::2]
            if self.data_type == 'float':
                data_arr = np.array([data], dtype=np.int32)
                data_as_float = data_arr.view(dtype=np.float32).tolist()[0]  # to list zmienia na liste i pomija [[]]
                data = data_as_float
            if self.data_type == 'int32':
                data_arr = np.array([data], dtype=np.int32)
                data_as_int32 = data_arr.view(dtype=np.int32).tolist()[0]  # to list zmienia na liste i pomija [[]]
                data = data_as_int32
        return data

    def _data_to_dict(self, data):
        '''
        Wrzuca ponumerowane rejestry do slownika
        :param data: Lista z pobranymi rejestrami
        :return: Slownik.
        '''
        if self.data_type == 'int' or self.data_type == 'bool':
            dic_val = {str(nr + self.reg_start): v for nr, v in enumerate(data)}
        else:
            dic_val = {str(nr + self.reg_start): v for nr, v in enumerate(data[::2])}  # 0,2,4,6
        return_dict = {'Device': self.unit, 'Reg_type': self.reg_type, 'Data_type': self.data_type, 'Data': dic_val}
        return return_dict

    # ------------------------------------------------------------------------------------------------------------------
    # metody uruchomieniowe
    def read_bool(self, unit, reg_start, reg_lenght, reg_type='coil'):
        '''
        Odczytanie rejestrow binarnych.
        :param unit: Adres urzadzenia.
        :param reg_start: Rejestr początkowy.
        :param reg_lenght: Dlugosc zapytania.
        :param reg_type: Typ rejestru.
        :return: Slownik
        '''
        self.unit = unit
        self.reg_start = reg_start
        self.reg_lenght = reg_lenght
        self.reg_type = reg_type
        self.data_type = 'bool'

        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        if self.reg_type == 'coil':
            measure = self._read_multiple_colis()
        elif self.reg_type == 'disc_input':
            measure = self._read_multipe_discrete_inputs()
        else:
            print("Zly typ rejstru")
        self.client.close()
        if measure != False:
            data_ok = self._data_check(measure)
            if data_ok:
                dicData = self._data_to_dict(measure)  # zamiana na slownik i wydruk
                return dicData

    def write_register(self,unit, reg_add, new_val):
        '''
        Zapis jednego rejestru
        :param unit: Adres urzadzenia.
        :param reg_add: Adres rejetru do zapisu.
        :param new_val: Nowa wartosc rejestru
        :return: list(unit,reg_add,new_val]
        '''
        self.reg_add = reg_add
        self.new_val = new_val
        self.unit = unit

        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        self._write_single()
        self.client.close()
        return self.unit,self.reg_add,self.new_val

    def read_register(self, unit, reg_start, reg_lenght, reg_type='holding', data_type='int', transp=False):
        '''

        :param unit: Adres urzadznia.
        :param reg_start: Rejestr początkowy.
        :param reg_lenght: Dlugosc zapytania.
        :param reg_type: Typ rejestru. ('holding','input','coil','disc_input')
        :param data_type: Typ danych ('int','int32','float')
        :param transp: odwrócenie rejestrow.
        :return: Slownik
        '''
        self.unit = unit
        self.reg_start = reg_start
        self.reg_lenght = reg_lenght
        self.reg_type = reg_type
        self.data_type = data_type
        self.transp = transp
        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        time.sleep(0.0)
        if self.reg_type == 'holding':
            data = self._read_holding()
        elif self.reg_type == "input":
            data = self._read_input()
        self.client.close()
        if data != False:
            data_ok = self._data_check(data)
            if data_ok:
                d_type = self._choise_data_type(data)  # wynik odczytu jako lista w zaleznosci od traspozycji
                dicData = self._data_to_dict(d_type)  # zamiana na slownik i wydruk
                return dicData


# ===================================================================================================================

if __name__ == '__main__':

    staski = TCP_Client('37.26.192.248', 502)
    print("host:",staski.client.host)
    print("time out:",staski.client.timeout)

    conn = Master(staski.client)
    try:
        reg = conn.read_register(1, 101, 10, reg_type='holding', data_type='int')
        print(reg)
    except Exception as e:
        print(e)


    staski = TCP_Client('37.26.192.248', 502)
    conn = Master(staski.client)
    try:
        coil = conn.read_bool(1, 0, 250, reg_type='coil')
        input_reg = conn.read_bool(1, 1000, 250, reg_type='coil')
        print(coil)
        print(input_reg)
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
    #
    # cofowent = TCP_Client('192.168.0.30', 502)
    # cofowent_conn = Master(cofowent.client)
    # reg_cofowent = cofowent_conn.read_register(5, 0, 10, reg_type='holding', data_type='int')
    # print(reg_cofowent)
