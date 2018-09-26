#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymodbus.client.sync import ModbusTcpClient as ModbusClient
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




class Master():
    ''' Obsłoga Modbus RTU'''

    def __init__(self, host,port):
        self.host = host
        self.port = port
        self.client = ModbusClient(host=self.host,port=self.port,timeout=3)
        self.connection = self.client.connect()
        print(
            "Connection: {}\nhost = {},\nport = {}".format(
                self.connection,
                self.host,
                self.port, ))

    def read_register(self, unit, reg_start, reg_lenght, reg_type='holding', data_type='int'):
        """Funkcja glowna odczytu rejestrow, wywolujaca inne podfunkcje"""
        # TODO: Nie wiem czy nazwa jest prawidlowa. Niby czyta rejestry ale tak naprawde obsluguje odczyt
        # TODO: Jeszcze bardziej rozdzielic zadania funkcji na mniejsze funkcje

        parm = [unit, reg_start, reg_lenght]
        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        time.sleep(0.0)
        if reg_type == 'holding':
            data = self.read_holding( parm)
        elif reg_type == "input":
            data = self.read_input( parm)
        self.client.close()
        measure = self.choise_data_type(data, data_type)
        self.display_data(measure,unit,reg_start)
        return measure
    def write_register(self, reg_add,val,unit):
        #print(self.client.connect())
        # self.client.connect()
        # print(self.client.connect())
        parm=[unit,reg_add,val]
        self.write_single_register(parm)
        self.client.close()

        return print('Nowa wartosc zapisana')

    def read_holding(self, parm):
        try:
            massure = self.client.read_holding_registers(parm[1], parm[2], unit=parm[0])
            #self.assercion(massure)
            print(massure)
            return massure.registers[0:]
        except AttributeError:
            print('modbus error')
            return ['NoN']



    def read_input(self, parm):
        massure = self.client.read_input_registers(parm[1], parm[2], unit=parm[0])
        return massure.registers[0:]

    def write_single_register(self,parm):
        rq=self.client.write_register(parm[1], parm[2], unit=parm[0])
        print(self.client._wait_for_data())
        rr= self.client.read_holding_registers(parm[1],1,unit=parm[0])
        self.assercion(rq)
        assert (rr.registers[0] == parm[2]) # test the expected value

    def assercion(self,operation):
        # test that we are not an error
        if not operation.isError():
            print("Nie ma erroru")
        else:
            print(" Jest error")



    def check_write(self,parm):
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

    def display_data(self, data,unit,reg_start):
        dic_val={}
        for nr,v in enumerate(data):
            dic_val[nr+reg_start]=v
        print("Urzadzenie {} - {}".format(str(unit),dic_val))


# TODO: DODAC ZAPIS REJSTROW
# TODO: DODAC POMNIEJSZE WYSPECIALIZOWANE MODULY DO ZMIANY ADRESU PREDKOSCI I MOZE JAKIS INNNE

if __name__ == '__main__':
    apar = Master(host='192.168.10.11', port=503)
    print(apar.connection)
    while apar.connection:
        units=list(range(1,33))
        print(units)
        for i in units:
            apar.read_register(i, 0, 4)
            time.sleep(0)
        print(160*"=")
