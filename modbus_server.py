from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusSlaveContext
import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class LoggingDataBlock(ModbusSequentialDataBlock):    
    def __init__(self, register_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_type = register_type

    def getValues(self, address, count=1):
        logger.info(f"READ {self.register_type} - Address: {address}, Count: {count}")
        return super().getValues(address, count)

    def setValues(self, address, values):
        logger.info(f"WRITE {self.register_type} - Address: {address}, Values: {values}")
        super().setValues(address, values)

def run_server():
    store = ModbusSlaveContext(
        hr=LoggingDataBlock("Holding Register", 0, [0] * 100),  # Read/write
        ir=LoggingDataBlock("Input Register", 0, [0] * 100),    # Read-only
        co=LoggingDataBlock("Coil", 0, [0] * 100),              # Read/write (binary)
        di=LoggingDataBlock("Discrete Input", 0, [0] * 100)      # Read-only (binary)
    )

    context = ModbusServerContext(slaves=store, single=True)
    
    StartTcpServer(
        context=context,
        address=("localhost", 5020)
    )

if __name__ == "__main__":
    run_server()