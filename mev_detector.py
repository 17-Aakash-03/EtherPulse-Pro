import pandas as pd
from alerts import send_alert

def detect_mev(tx_list):
    """
    Scans a list of transactions for MEV signatures:
    1. High Gas Price (Priority Fees)
    2. Multiple transactions from the same sender in one burst.
    """
    df = pd.DataFrame(tx_list)
    
    # 1. Group by sender to find 'High Velocity' wallets
    counts = df['from'].value_counts()
    
    for address, count in counts.items():
        if count > 2:  # If one wallet is spamming trades in seconds
            # 2. Check if they are paying high gas
            address_txs = df[df['from'] == address]
            avg_gas = address_txs['gas_gwei'].mean()
            
            if avg_gas > 50: # If they are paying 50+ Gwei to 'cut in line'
                msg = f"🛡️ MEV BOT DETECTED!\nAddr: {address[:10]}...\nGas: {avg_gas:.2f} Gwei\nActivity: {count} TXs in burst."
                send_alert(msg)
                return True
    return False

# Simulated Test Data
test_mempool = [
    {'from': '0xBot123...', 'gas_gwei': 120, 'value': 0.1},
    {'from': '0xBot123...', 'gas_gwei': 125, 'value': 0.1},
    {'from': '0xBot123...', 'gas_gwei': 118, 'value': 0.1},
    {'from': '0xUser...', 'gas_gwei': 10, 'value': 5.0}
]

if __name__ == "__main__":
    print("🤖 Scanning simulated mempool for MEV...")
    detect_mev(test_mempool)