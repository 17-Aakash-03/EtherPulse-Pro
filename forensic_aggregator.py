import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models

# 1. Load Data
df = pd.read_csv("cleaned_data.csv")
X = df[['eth_value', 'gas_gwei', 'time_diff']].values

# --- WHALE DETECTIVE (XGBoost) ---
# We'll label anything over 10 ETH as a 'Whale' (Class 1)
y_whale = (df['eth_value'] > 10).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y_whale, test_size=0.2)

whale_model = xgb.XGBClassifier()
whale_model.fit(X_train, y_train)
whale_model.save_model("whale_detective.json")
print("✅ Whale Detective Trained!")

# --- SCAM DETECTIVE (Autoencoder) ---
# It learns what 'Normal' looks like. If it can't rebuild a transaction, it's a SCAM.
input_dim = X.shape[1]
encoding_dim = 2

input_layer = layers.Input(shape=(input_dim,))
encoder = layers.Dense(encoding_dim, activation="relu")(input_layer)
decoder = layers.Dense(input_dim, activation="sigmoid")(encoder)

autoencoder = models.Model(inputs=input_layer, outputs=decoder)
autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.fit(X, X, epochs=10, batch_size=32, verbose=0)

autoencoder.save("scam_detective.keras")
print("✅ Scam Detective Trained!")