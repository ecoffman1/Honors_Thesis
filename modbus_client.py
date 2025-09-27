from pymodbus.client import ModbusTcpClient
from config import (
    MODBUS_HOST, MODBUS_PORT, REGISTER_COUNT, SLAVE_ID,
    SOLID_SERVER, RESOURCE_URL, OIDC_ISSUER, CSS_EMAIL, CSS_PASSWORD
)

def test_client():
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    client.connect()

    value = input("Enter a integer to store: ")
    registerNumber = input("To what register: ")
    client.write_register(address=int(registerNumber), value=int(value), slave=SLAVE_ID)
    client.close()

if __name__ == "__main__":
    test_client()