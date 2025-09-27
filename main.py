import time
from config import (
    MODBUS_HOST, MODBUS_PORT, SLAVE_ID,
    SOLID_SERVER, RESOURCE_URL, OIDC_ISSUER, CSS_EMAIL, CSS_PASSWORD
)
from handlers.modbus_handler import load_modbus_mappings, get_register_metadata
from utils import add_context
from handlers.solid_handler import CssAccount, get_client_credentials, append_to_solid

func_codes = {
    1: "Read the status of output coils",
    2: "Read the status of input coils",
    3: "Read 16-bit values from holding registers",
    4: "Read 16-bit values from input registers",
    5: "Write to a single output coil",
    6: "Write a 16-bit value to a single holding register",
    15: "Write to multiple output coils",
    16: "Write 16-bit values to multiple holding registers",
    22: "Modifies specific bits within a holding register",
}

# Reading and uploading RDF for a specified register
def process_register(slave_id, func_code, register_address, modbus_value):
    # Load the Modbus mappings from the JSON file
    modbus_mappings = load_modbus_mappings("modbus_mappings2.json")

    # Get metadata for the specified register
    register_metadata = get_register_metadata(register_address, modbus_mappings)

    if register_metadata:
        # Attach context RDF style using the register metadata
        rdf_data = add_context(
            slave_id=slave_id,
            register=register_address,
            function=register_metadata["function"],
            func_code=func_codes[func_code],
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
            process_register(2,3, register_address,25)
        except ValueError:
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()
