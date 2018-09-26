#!/usr/bin/env python
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




class Master():
    ''' Obsłoga Modbus RTU'''

    def __init__(self,speed,port, method='rtu',stopbits=1, parity='N', bytesize=8, timeout=1):
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
        print(
            "Connection: {}\nmethod = {},\nport = {},\nbaudrate = {},\nstopbits = {},\nparity = {},\nbytesize = {},\ntimeout = {},\n".format(
                self.connection,
                self.method,
                self.port,
                self.speed,
                self.stopbits,
                self.parity,
                self.bytesize,
                self.timeout, ))

    def read_register(self, unit, reg_start, reg_lenght, reg_type='holding', data_type='int'):
        """Funkcja glowna odczytu rejestrow, wywolujaca inne podfunkcje"""
        # TODO: Nie wiem czy nazwa jest prawidlowa. Niby czyta rejestry ale tak naprawde obsluguje odczyt
        # TODO: Jeszcze bardziej rozdzielic zadania funkcji na mniejsze funkcje

        parm = [unit, reg_start, reg_lenght]
        self.client.connect()  # TO CHYBA POTRZEBNE JEZELI ZAMYCKAM SESJE PRZY KAZDYM KONCU POMIARU
        time.sleep(0.2)
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
        massure = self.client.read_holding_registers(parm[1], parm[2], unit=parm[0])
        #sprawdzenie czy nie ma errorow
        if self.assercion(massure,parm[0])==False:

            return massure.registers[0:]
        else:
            return False

    def read_input(self, parm):
        massure = self.client.read_input_registers(parm[1], parm[2], unit=parm[0])
        return massure.registers[0:]

    def write_single_register(self,parm):
        self.client.write_register(parm[1], parm[2], unit=parm[0])
        # print(self.client._wait_for_data())
        # rr= self.client.read_holding_registers(parm[1],1,unit=parm[0])
        # self.assercion(rq)
        # assert (rr.registers[0] == parm[2]) # test the expected value

    def assercion(self,operation,unit):
        # test that we are not an error
        if not operation.isError():
            pass
        else:
            print("Bład polaczenia z adresem ",unit)
        return operation.isError()



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
        if data!=False:
            for nr,v in enumerate(data):
                dic_val[nr+reg_start]=v
            print("Urzadzenie {} - {}".format(str(unit),dic_val))
        else:
            pass



# TODO: DODAC ZAPIS REJSTROW
# TODO: DODAC POMNIEJSZE WYSPECIALIZOWANE MODULY DO ZMIANY ADRESU PREDKOSCI I MOZE JAKIS INNNE

if __name__ == '__main__':
    # apar = Master(port='com3', speed=2400)
    # fif = Master(port='com2', speed=9600)
    # connections = [apar]
    # for nr, conn in enumerate(connections):
    #     if conn.connection == False:
    # #         print("Polaczenie: ", nr, "False!!!!!!!!!!")
    # print(apar.connection)
    # while apar.connection:
    #     units=[17,18,23,22]
    #     for i in units:
    #         apar.read_register(i, 0, 30)
    #         time.sleep(0.5)
    #     print(160*"=")





    def speed_change(units,speedOld,speedNew):
        # czesc o zmianie adresow

        '''
        115,2k  -   9
        57,6k   -   8
        38,4k   -   7
        19,2k   -   6
        14,4k   -   5
        9,6k    -   4
        4,8k    -   3
        2,4k    -   2
        1,2k    -   1
        0,6k    -   0
        '''
        speedTab={ 0:600,1:1200,2:2400,3:4800,4:9600,5:14400,6:19200,7:38400,8:57600,9:115200}
        for unit in units:
            apar1 = Master(port='com3', speed=speedOld)
            if apar1.connection == True:
                print(30*"=")
                print("\nOdczytanie rejestrow z unit nr:",unit)
                reg = apar1.read_register(unit, 29, 1)
                time.sleep(0.5)
                print(160 * "=")
                if reg != False:
                    testVar = input("Czy chcesz zmienic adres z {} na {} ( t/n).".format(speedTab[reg[0]],speedNew))
                    if testVar != "t":
                        print("Wyjscie z programu")
                    else:
                        print("Zmiana adresu na " ,speedNew)
                        # przypisanie nowej awrtosci rejestru
                        for k,v in speedTab.items():
                            if v==speedNew:
                                regVal=k
                                print("{} = {}".format(v,k))
                            else:
                                pass
                        print("Nowa Wartosc ",regVal)
                        time.sleep(0.5)
                        apar1.write_register(29, regVal, unit)
                        time.sleep(0.5)
                        print("Sprawdzenie połaczenia")
                        apar2 = Master(port='com3', speed=speedNew)
                        reg2 = apar2.read_register(unit, 29, 1)
                        time.sleep(1)


    def unitCheck(start,stop,speed):
        units=[]
        apar=Master(port='com3', speed=speed)
        while apar.connection == True:
            for unit in range(start,stop+1):
                conn = apar.read_register(unit, 29, 1)
                print(conn)
                if conn!=False:
                    units.append(unit)
                if unit==stop:
                    break
            break
        print(units)
        return units


    units=unitCheck(15,25,2400)
    speed_change(units,2400,2400)










