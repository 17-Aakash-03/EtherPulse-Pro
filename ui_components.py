import asyncio
import websockets
import json
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from web3 import Web3

# --- SETUP ---
WSS_URL = "wss://eth-mainnet.g.alchemy.com/v2/z397HVvwuUVderkybJ2-W"
HTTP_URL = "https://eth-mainnet.g.alchemy.com/v2/z397HVvwuUVderkybJ2-W"
w3 = Web3(Web3.HTTPProvider(HTTP_URL))

# 1. Load the Detectives
lstm_model = load_model("gas_detective.h5")
transformer_model = load_model("transformer_detective.keras")

# 2. Setup the Scaler (We need this to talk to the AI)
# We use the original cleaned data to make sure the "scaling" is the same
df = pd.read_csv("cleaned_data.csv")
scaler = MinMaxScaler()
scaler.fit(df[['eth_value', 'gas_gwei', 'time_diff']].values)

# Memory for the AI (rolling window of 10)
memory = []

async def live_dashboard():
    global memory
    async with websockets.connect(WSS_URL) as ws:
        await ws.send(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}))
        
        print("\n" + "="*50)
        print("🚀 ETHERPULSE LIVE AI DASHBOARD")
        print("Comparing: LSTM vs TRANSFORMER")
        print("="*50 + "\n")

        last_time = None

        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if "params" in data:
                tx_hash = data["params"]["result"]
                try:
                    tx = w3.eth.get_transaction(tx_hash)
                    if tx:
                        # Extract Features
                        eth_val = float(w3.from_wei(tx['value'], 'ether'))
                        gas_gwei = tx['gasPrice'] / 10**9
                        
                        current_time = pd.Timestamp.now()
                        time_diff = (current_time - last_time).total_seconds() if last_time else 0
                        last_time = current_time

                        # Update AI Memory
                        new_row = [eth_val, gas_gwei, time_diff]
                        scaled_row = scaler.transform([new_row])[0]
                        memory.append(scaled_row)

                        if len(memory) > 10:
                            memory.pop(0)
                            
                            # Prepare data for AI
                            input_data = np.array([memory])

                            # PREDICT!
                            lstm_pred = lstm_model.predict(input_data, verbose=0)[0][0]
                            trans_pred = transformer_model.predict(input_data, verbose=0)[0][0]

                            # De-scale the prediction back to real Gwei
                            # (Quick hack: just use the Gwei column from scaler)
                            dummy = np.zeros((1, 3))
                            dummy[0, 1] = lstm_pred
                            lstm_final = scaler.inverse_transform(dummy)[0, 1]
                            
                            dummy[0, 1] = trans_pred
                            trans_final = scaler.inverse_transform(dummy)[0, 1]

                            print(f"TX: {tx_hash[:10]}... | Value: {eth_val:.4f} ETH")
                            print(f"   📉 LSTM Predicts Next Gas: {lstm_final:.2f} Gwei")
                            print(f"   🤖 TRANSFORMER Predicts:  {trans_final:.2f} Gwei")
                            print("-" * 40)
                except:
                    pass

asyncio.run(live_dashboard())