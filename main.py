import time
from config import (
    MODBUS_HOST, MODBUS_PORT, SLAVE_ID,
    SOLID_SERVER, RESOURCE_URL, OIDC_ISSUER, CSS_EMAIL, CSS_PASSWORD
)
from handlers.modbus_handler import read_modbus_value, load_modbus_mappings, get_register_metadata
from utils import add_context
from handlers.solid_handler import CssAccount, get_client_credentials, append_to_solid

# Reading and uploading RDF for a specified register
def process_register(register_address):
    # Read Modbus
    try:
        modbus_value = read_modbus_value(MODBUS_HOST, MODBUS_PORT, register_address, 1, SLAVE_ID)
        print(f"Modbus Value from register {register_address}: {modbus_value}")
    except Exception as e:
        print(f"Error reading Modbus data for register {register_address}: {e}")
        return

    # Load the Modbus mappings from the JSON file
    modbus_mappings = load_modbus_mappings()

    # Get metadata for the specified register
    register_metadata = get_register_metadata(register_address, modbus_mappings)

    if register_metadata:
        # Attach context RDF style using the register metadata
        rdf_data = add_context(
            register=register_metadata["register"],
            function=register_metadata["function"],
            value=modbus_value,
            data_type=register_metadata["type"],
            notes=register_metadata["notes"],
            timestamp=int(time.time())
        )
        print("RDF:\n", rdf_data)

        # Authentication
        account = CssAccount(css_base_url=SOLID_SERVER, email=CSS_EMAIL, password=CSS_PASSWORD)

        try:
            client_credentials = get_client_credentials(account)
            CLIENT_ID = client_credentials.client_id
            CLIENT_SECRET = client_credentials.client_secret
            print(f"Client ID: {CLIENT_ID}")
        except Exception as e:
            print(f"Error fetching client credentials: {e}")
            return

        # Upload to Solid Pod
        result = append_to_solid(OIDC_ISSUER, CLIENT_ID, CLIENT_SECRET, RESOURCE_URL, rdf_data)
        print(result)
    else:
        print(f"Register {register_address} not found in mappings.")

def main():
    while True:
        try:
            register_address = int(input("Enter the Modbus register address to read from (or type 'exit' to quit): "))
            process_register(register_address)
        except ValueError:
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()
