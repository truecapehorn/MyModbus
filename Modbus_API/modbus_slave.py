#!/usr/bin/env python

from pymodbus.server.sync import StartTcpServer, ModbusTcpServer
from pymodbus.server.sync import StartUdpServer
from pymodbus.server.sync import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

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

    def create_contexts(self):
        slaves = {}
        for i in range(self.id_start,self.id_range+1):
            slaves[i]=ModbusSlaveContext(
                di=ModbusSequentialDataBlock(0, [0] * 255),
                co=ModbusSequentialDataBlock(0, [0] * 255),
                hr=ModbusSequentialDataBlock(0, [0] * 255),
                ir=ModbusSequentialDataBlock(0, [0] * 255))
        self.context = ModbusServerContext(slaves=slaves, single=False)

        return self.context




class TCP_slave(Slave):
    def __init__(self,id_start,id_range,host ='localhost',port = 5020):
        super().__init__(id_start,id_range)
        self.host = host
        self.port= port

    def run_server(self):
        context = self.create_contexts()
        address=(self.host, self.port)
        print(address)

        try:
            # StartTcpServer(context, identity=identity, address=(self.host, self.port))
            ModbusTcpServer(context, identity=identity, address=(self.host, self.port))


        except Exception as e:
            print(e)





if __name__=='__main__':


    # sl=Slave(1,20)
    # context=sl.create_contexts()
    # StartTcpServer(context, identity=identity, address=("localhost", 5021))

    sl2 = TCP_slave(1,20,port=5027)
    sl2.run_server()








