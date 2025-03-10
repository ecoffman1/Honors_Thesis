from pymodbus.client import ModbusTcpClient

def test_client():
    client = ModbusTcpClient('localhost', port=5020)
    client.connect()

    userInput = input("Enter a integer to store: ")
    client.write_register(address=0, value=int(userInput), slave=0)
    client.close()

if __name__ == "__main__":
    test_client()