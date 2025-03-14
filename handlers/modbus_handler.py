import json
from pymodbus.client import ModbusTcpClient

def read_modbus_value(host, port, address, count, slave_id):
    client = ModbusTcpClient(host, port=port)
    response = client.read_holding_registers(address, count=count, slave=slave_id)
    client.close()

    if response.isError():
        raise Exception("Error reading Modbus data")

    return response.registers[0]

def load_modbus_mappings(file_path="modbus_mappings.json"):
    with open(file_path, "r") as f:
        return json.load(f)
    
def get_register_metadata(register_address, mappings):
    for register in mappings["registers"]:
        if register["register"] == register_address:
            return register
    return None