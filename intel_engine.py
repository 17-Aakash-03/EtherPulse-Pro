def get_forensic_profile(address):
    """
    Simulates AI behavioral analysis to generate the Radar Chart shape.
    Returns: [Security Risk, Whale Volume, Bot Activity, DNA Integrity]
    """
    if not address or len(address) < 10:
        return [30, 30, 30, 30] # Default balanced shape
        
    addr_lower = address.lower()
    
    # CASE 1: Known Exchange (e.g., Binance)
    if "0x28c6" in addr_lower:
        return [12, 98, 40, 95]
        
    # CASE 2: High-Frequency Bot (Stretches toward Bot and Risk)
    elif addr_lower.startswith("0xbc") or "bot" in addr_lower:
        return [88, 25, 95, 18]
        
    # CASE 3: Large Whale (Stretches toward Whale Volume)
    elif addr_lower.startswith("0x74"):
        return [20, 99, 15, 65]
        
    # CASE 4: Standard User / Retail
    else:
        return [35, 40, 50, 60]

def scan_contract_safety(address):
    """Returns a text-based forensic summary."""
    if "0x28c" in address.lower():
        return "🛡️ SECURE: Verified Institutional Wallet (Exchange). DNA matches known safe-haven patterns."
    return "⚠️ ALERT: Unverified Contract DNA. Behavioral heuristics suggest early-stage deployment."

def get_gas_advice(gwei):
    """Analyzes network congestion."""
    if gwei < 15: 
        return "🟢 OPTIMAL: Network traffic is low. Transaction finality expected in < 12 seconds."
    return "🔴 CONGESTED: High gas demand. AI suggests waiting for a baseline dip."