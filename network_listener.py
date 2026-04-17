import asyncio
import websockets
import json

# Your API key is already inside this link
ALCHEMY_WSS_URL = "wss://eth-mainnet.g.alchemy.com/v2/z397HVvwuUVderkybJ2-W"

async def listen_to_mempool():
    # This opens the "Phone Call" to the blockchain
    async with websockets.connect(ALCHEMY_WSS_URL) as ws:
        # This tells the blockchain: "Send me everything!"
        subscription_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_subscribe",
            "params": ["newPendingTransactions"]
        }
        await ws.send(json.dumps(subscription_request))
        
        print("--- LISTENING TO LIVE ETHEREUM NETWORK ---")

        while True:
            try:
                message = await ws.recv()
                data = json.loads(message)
                
                if "params" in data:
                    tx_hash = data["params"]["result"]
                    print(f"New Transaction Detected! ID: {tx_hash}")
                    
            except Exception as e:
                print(f"Error: {e}")
                break

# This starts the script
asyncio.run(listen_to_mempool())