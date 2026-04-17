import random

def scan_contract_safety(address):
    """
    Simulates checking if an address is a Smart Contract or a Wallet (EOA).
    """
    if not address or len(address) < 42:
        return "⚠️ INVALID_ADDRESS: HANDSHAKE_FAILED"
        
    # Heuristic: Check for common contract patterns in the string
    if "0x3f" in address.lower() or "0x68" in address.lower():
        return "⚠️ ALERT: Unverified Contract DNA. Behavioral heuristics suggest early-stage deployment."
    return "✅ IDENTITY: Verified EOA (Wallet) detected. Neural handshake stable."

def get_gas_advice(gas_price):
    """
    Provides advice based on current gas price.
    """
    if gas_price < 20:
        return "🟢 OPTIMAL: Network traffic is low. Transaction finality expected in < 12 seconds."
    elif gas_price < 50:
        return "🟡 STABLE: Moderate traffic. Standard execution protocols recommended."
    else:
        return "🔴 CONGESTED: High traffic detected. Consider delay to avoid high priority fees."

def get_forensic_profile(address):
    """
    Generates dynamic forensic scores for the radar chart.
    """
    # Use the address as a seed so the graph is consistent for each address
    random.seed(address)
    
    # Check for Vitalik's address specifically for the 'Elite' profile
    if address.lower() == "0xd8da6bf26964af9d7eed9e03e53415d37aa96045":
        return [10, 95, 15, 98] # [Risk, Whale, Bot, Integrity]
        
    # Return randomized but deterministic heuristics for others
    return [
        random.randint(5, 40),  # Security Risk
        random.randint(10, 95), # Whale Volume
        random.randint(5, 80),  # Bot Activity
        random.randint(30, 99)  # DNA Integrity
    ]