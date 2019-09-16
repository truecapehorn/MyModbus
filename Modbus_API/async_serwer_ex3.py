from pymodbus.server.asynchronous import StartTcpServer, StopServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

import threading
import sys
import logging

FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def stop():
    print('Process will be down.')
    StopServer()  # Stop server.
    sys.exit(0)  # Kill the server code.

def run_async_server():
    store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [17] * 100))
    slaves = {
        0x01: store,
        0x02: store,
        0x03: store,
    }
    context = ModbusServerContext(slaves=slaves, single=False)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '1.5'

    from twisted.internet import reactor
    StartTcpServer(context, identity=identity, address=("localhost", 5020),
                   defer_reactor_run=True)
    print('Start an async server.')
    t = threading.Timer(5, stop)
    t.daemon = True
    t.start()
    reactor.run()
    print('Server was stopped.')
    help(reactor)

if __name__ == "__main__":
    run_async_server()