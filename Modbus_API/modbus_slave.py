#!/usr/bin/env python

# from pymodbus.server.sync import StartTcpServer
from pymodbus.server.sync import StartUdpServer
from pymodbus.server.sync import StartSerialServer

from pymodbus.server.asynchronous import StartTcpServer,StopServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from twisted.internet.task import LoopingCall


import time

from pymodbus.transaction import ModbusRtuFramer
#---------------------------------------------------------------------------#
# configure the service logging
#---------------------------------------------------------------------------#
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


#---------------------------------------------------------------------------#
# initialize your data store
#---------------------------------------------------------------------------#

identity = ModbusDeviceIdentification()
identity.VendorName  = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl   = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName   = 'Pymodbus Server'
identity.MajorMinorRevision = '1.0'



class Slave:
    def __init__(self,id_start,id_range):
        self.id_start = id_start
        self.id_range = id_range

    def create_context(self):
        slaves = {}
        for i in range(self.id_start,self.id_range+1):
            slaves[i]=ModbusSlaveContext(
                di=ModbusSequentialDataBlock(0, [0] * 255),
                co=ModbusSequentialDataBlock(0, [0] * 255),
                hr=ModbusSequentialDataBlock(0, [0] * 255),
                ir=ModbusSequentialDataBlock(0, [0] * 255))
        self.context = ModbusServerContext(slaves=slaves, single=False)

        return self.context

    def updating_writer(self,a):
        self.a =a
        ''' A worker process that runs every so often and
        updates live values of the context. It should be noted
        that there is a race condition for the update.

        :param arguments: The input arguments to the call
        '''
        log.debug("updating the context")
        context = self.a[0] # ModbusSlaveContext
        register = 3  # ? the function we are working with 3 holding 4 input
        slave_id = 0x01  # ? Adres slave dla ktorego chcemy zmienic wartosc
        address = 0x10  # 17 rejestr
        # todo: odczytanie jsona
        values = context[slave_id].getValues(register, address, count=5)  # pobranie contextu z tla
        # todo: jezli valuses_plik != values : to zapis do pliku
        # todo: trzeba podzielic rejestry do zapisu i do odczytu,
        # todo: rejetry wr to beda mialy priorytet zapisu

        values = [v + 1 for v in values]  # zwikszenie rejestru
        log.debug("new values: " + str(values))
        context[slave_id].setValues(register, address, values)  # ustawineie rejestru





class TCP_slave(Slave):
    def __init__(self,id_start,id_range,host ='localhost',port = 5020):
        super().__init__(id_start,id_range)
        self.host = host
        self.port= port

    def run_server(self):
        context = self.create_context()
        address=(self.host, self.port)
        print(address)

        try:
            cycle = 5  # 5 seconds delay
            loop = LoopingCall(f=self.updating_writer, a=(context,))
            loop.start(cycle, now=False)  # initially delay by time
            StartTcpServer(context, identity=identity, address=(self.host, self.port),defer_reactor_run=False)

        except KeyboardInterrupt:
            print('Koniec')
            StopServer()





if __name__=='__main__':


    # sl=Slave(1,20)
    # context=sl.create_contexts()
    # StartTcpServer(context, identity=identity, address=("localhost", 5021))

    sl2 = TCP_slave(1,20,port=5027)
    sl2.run_server()








