import asyncio
import websockets
import json
import psycopg2
from web3 import Web3

# --- CONFIGURATION ---
# The "Phone Numbers" for the blockchain
WSS_URL = "wss://eth-mainnet.g.alchemy.com/v2/z397HVvwuUVderkybJ2-W"
HTTP_URL = "https://eth-mainnet.g.alchemy.com/v2/z397HVvwuUVderkybJ2-W"

# Your Database credentials
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "postgres123" 
DB_HOST = "localhost"
DB_PORT = "5432"

# Connect to the blockchain "Translator"
w3 = Web3(Web3.HTTPProvider(HTTP_URL))

def save_to_db(tx_hash, sender, receiver, value, gas):
    try:
        # Connect to the Cabinet
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        cursor = conn.cursor()

        # The command to save the data
        query = """INSERT INTO raw_transactions (tx_hash, sender, receiver, eth_value, gas_price) 
                   VALUES (%s, %s, %s, %s, %s) ON CONFLICT (tx_hash) DO NOTHING"""
        
        cursor.execute(query, (tx_hash, sender, receiver, value, gas))
        conn.commit()
        
        print(f"✅ Saved to DB: {tx_hash[:10]}... | {value} ETH")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ DB Error: {e}")

async def listen_and_save():
    async with websockets.connect(WSS_URL) as ws:
        # Subscribe to the live feed
        await ws.send(json.dumps({
            "jsonrpc": "2.0", "id": 1, 
            "method": "eth_subscribe", "params": ["newPendingTransactions"]
        }))
        
        print("--- STARTING LIVE DATA COLLECTION ---")
        print("Press Ctrl+C to stop when you have enough data.")

        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if "params" in data:
                tx_hash = data["params"]["result"]
                try:
                    # Ask the blockchain for the details of this ID
                    tx = w3.eth.get_transaction(tx_hash)
                    if tx:
                        eth_val = float(w3.from_wei(tx['value'], 'ether'))
                        # Send it to the Database
                        save_to_db(tx_hash, tx['from'], tx['to'], eth_val, tx['gasPrice'])
                except:
                    # Some transactions are too fast to catch, that's okay!
                    pass

# RUN THE SCRIPT
asyncio.run(listen_and_save())