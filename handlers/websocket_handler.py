import json
import time
import websockets
import requests
import ssl
from solid_client_credentials import SolidClientCredentialsAuth, DpopTokenProvider
from handlers.solid_handler import ClientCredentials

async def listen_to_websocket(websocket_url, callback):
    ssl_context = ssl._create_unverified_context()

    async with websockets.connect(websocket_url, ssl=ssl_context) as websocket:
        print(f"Connected to WebSocket: {websocket_url}")
        while True:
            message = await websocket.recv()
            print(f"Received message: {message} [{time.time() * 1000}]")
            callback(json.loads(message)["object"])

def get_websocket_url(css_base_url, oidc_issuer, client_credentials: ClientCredentials, topic_url):
    token_provider = DpopTokenProvider(
        issuer_url=oidc_issuer, client_id=client_credentials.client_id, client_secret=client_credentials.client_secret
    )
    auth = SolidClientCredentialsAuth(token_provider)

    # Create JSON payload
    payload = {
        "@context": ["https://www.w3.org/ns/solid/notification/v1"],
        "type": "http://www.w3.org/ns/solid/notifications#WebSocketChannel2023",
        "topic": topic_url
    }

    headers = {
        "Content-Type": "application/ld+json"
    }

    # Make the POST request
    url = css_base_url + "/.notifications/WebSocketChannel2023/"
    response = requests.post(url, headers=headers, json=payload, auth=auth)

    # Check response status
    if response.status_code == 200:
        print("POST request successful")
        websocket_url = response.json().get("receiveFrom")
        print(f"WebSocket URL: {websocket_url}")
    else:
        print(f"POST request failed with status code {response.status_code}")
        print(response.text)
    
    return websocket_url
