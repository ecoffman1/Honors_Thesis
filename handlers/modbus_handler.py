import json
from pymodbus.client import ModbusTcpClient

def load_modbus_mappings(file_path="modbus_mappings.json"):
    with open(file_path, "r") as f:
        return json.load(f)
    
def get_register_metadata(register_address, mappings):
    for register in mappings["registers"]:
        if register["register"] == register_address:
            return register
    return None