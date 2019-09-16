from pymodbus.server.sync import StartTcpServer, ModbusTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import threading
import logging
import signal
import time

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

SERVER = None
THREADED_SERVER = None
LOOP = None

class ReusableModbusTcpServer(ModbusTcpServer):
    def __init__(self, context, framer=None, identity=None,
                 address=None, handler=None, **kwargs):
        self.allow_reuse_address = True
        ModbusTcpServer.__init__(self, context, framer, identity, address, handler, **kwargs)

class ThreadedModbusServer(threading.Thread):
    def __init__(self, server):
        super(ThreadedModbusServer, self).__init__(name="ModbusServerThread")
        self._server = server
        self.daemon = True

    def run(self):
        self._server.serve_forever()