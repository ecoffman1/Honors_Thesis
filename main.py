from config import (
    MODBUS_HOST, MODBUS_PORT, REGISTER_ADDRESS, REGISTER_COUNT, SLAVE_ID,
    SOLID_SERVER, RESOURCE_URL, OIDC_ISSUER, CSS_EMAIL, CSS_PASSWORD
)
from handlers.modbus_handler import read_modbus_value
from utils import add_context
from handlers.solid_handler import CssAccount, get_client_credentials, upload_to_solid

# Read Modbus
try:
    modbus_value = read_modbus_value(MODBUS_HOST, MODBUS_PORT, REGISTER_ADDRESS, REGISTER_COUNT, SLAVE_ID)
    print(f"Modbus Value: {modbus_value}")
except Exception as e:
    print(f"Error reading Modbus data: {e}")
    exit()

# Attach context RDF style
rdf_data = add_context(modbus_value)
print("RDF:\n", rdf_data)

# Authenticate
account = CssAccount(css_base_url=SOLID_SERVER, email=CSS_EMAIL, password=CSS_PASSWORD)

try:
    client_credentials = get_client_credentials(account)
    CLIENT_ID = client_credentials.client_id
    CLIENT_SECRET = client_credentials.client_secret
    print(f"Client ID: {CLIENT_ID}")
except Exception as e:
    print(f"Error fetching client credentials: {e}")
    exit()

# Upload to Solid Pod
result = upload_to_solid(OIDC_ISSUER, CLIENT_ID, CLIENT_SECRET, RESOURCE_URL, rdf_data)
print(result)
