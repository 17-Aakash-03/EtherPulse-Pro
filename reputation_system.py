def calculate_reputation(address, history):
    """
    Calculates a trust score based on behavior history.
    history = {'is_mev': bool, 'is_whale': bool, 'age_days': int}
    """
    score = 50  # Base Score
    
    if history['is_mev']:
        score -= 30
    if history['is_whale']:
        score += 20
    if history['age_days'] > 365:
        score += 15
        
    # Cap the score between 0 and 100
    final_score = max(0, min(100, score))
    
    if final_score > 70:
        status = "✅ TRUSTED"
    elif final_score < 40:
        status = "🚩 SUSPICIOUS"
    else:
        status = "⚖️ NEUTRAL"
        
    return final_score, status

# Test Cases
wallets = [
    {'addr': '0xSafe...', 'history': {'is_mev': False, 'is_whale': True, 'age_days': 400}},
    {'addr': '0xBot123...', 'history': {'is_mev': True, 'is_whale': False, 'age_days': 2}}
]

if __name__ == "__main__":
    for w in wallets:
        score, status = calculate_reputation(w['addr'], w['history'])
        print(f"Address: {w['addr']} | Score: {score} | Status: {status}")