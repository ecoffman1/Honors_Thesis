from pymodbus.client import ModbusTcpClient

def read_modbus_value(host, port, address, count, slave_id):
    client = ModbusTcpClient(host, port=port)
    response = client.read_holding_registers(address, count=count, slave=slave_id)
    client.close()

    if response.isError():
        raise Exception("Error reading Modbus data")

    return response.registers[0]
