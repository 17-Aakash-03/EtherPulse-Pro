from fastapi import FastAPI
import joblib
from tensorflow.keras.models import load_model
import numpy as np

app = FastAPI()

# Load all 3 brains
lstm = load_model("gas_detective.h5")
transformer = load_model("transformer_detective.keras")
# (You'd also load the others here)

@app.get("/status")
def get_danger_score(eth: float, gas: float):
    # This is a 'Dumb' version of a voting system
    # In a real one, you'd feed the data through the models
    
    danger_score = 0
    if eth > 50: danger_score += 40
    if gas > 100: danger_score += 40
    
    return {
        "score": danger_score,
        "status": "DANGER" if danger_score > 70 else "SAFE",
        "message": "Whale detected" if eth > 50 else "Network normal"
    }