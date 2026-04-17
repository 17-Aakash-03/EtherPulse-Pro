import asyncio
import websockets
import json
from web3 import Web3

# 1. Setup the connection
WSS_URL = "wss://eth-mainnet.g.alchemy.com/v2/z397HVvwuUVderkybJ2-W"
# We also need an HTTP link to "ask" for details (Alchemy provides this too)
HTTP_URL = "https://eth-mainnet.g.alchemy.com/v2/z397HVvwuUVderkybJ2-W"

w3 = Web3(Web3.HTTPProvider(HTTP_URL))

async def get_tx_details(tx_hash):
    try:
        # This is where we ask the blockchain: "What is inside this ID?"
        tx = w3.eth.get_transaction(tx_hash)
        
        if tx:
            # Feature 1: The Value (Converted from 'Wei' to 'ETH')
            eth_value = w3.from_wei(tx['value'], 'ether')
            
            # Feature 2: Gas Price (How much they paid to be fast)
            gas_price = tx['gasPrice']
            
            # Feature 3: From & To (Who is sending to whom?)
            sender = tx['from']
            receiver = tx['to']

            print(f"--- DATA EXTRACTED ---")
            print(f"Value: {eth_value} ETH")
            print(f"Sender: {sender}")
            print(f"Gas Price: {gas_price}")

            # DUMB LOGIC: The "Whale" Alert
            if eth_value > 10:  # If more than 10 ETH (~$25,000+)
                print("🚨🚨 WHALE DETECTED! BIG MONEY MOVING! 🚨🚨")
            print("-" * 30)

    except Exception:
        # Sometimes transactions disappear before we can look (that's normal)
        pass

async def listen_and_extract():
    async with websockets.connect(WSS_URL) as ws:
        # Subscribe to new transactions
        await ws.send(json.dumps({
            "jsonrpc": "2.0", "id": 1, 
            "method": "eth_subscribe", 
            "params": ["newPendingTransactions"]
        }))
        
        print("Listening for transactions and extracting features...")

        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if "params" in data:
                tx_hash = data["params"]["result"]
                # We tell the code to go look up the details for this ID
                await get_tx_details(tx_hash)

asyncio.run(listen_and_extract())