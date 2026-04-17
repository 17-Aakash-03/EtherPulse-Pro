import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras import layers, models

# 1. Load the food
df = pd.read_csv("cleaned_data.csv")
data = df[['eth_value', 'gas_gwei', 'time_diff']].values

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# 2. Create Sequences (Memory of 10)
X, y = [], []
for i in range(10, len(scaled_data)):
    X.append(scaled_data[i-10:i])
    y.append(scaled_data[i, 1])
X, y = np.array(X), np.array(y)

# 3. Build the Transformer Brain
def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0):
    # Attention Layer - This is the "Genius" part
    x = layers.MultiHeadAttention(key_dim=head_size, num_heads=num_heads, dropout=dropout)(inputs, inputs)
    x = layers.Dropout(dropout)(x)
    x = layers.LayerNormalization(epsilon=1e-6)(x)
    res = x + inputs

    # Feed Forward Part
    x = layers.Conv1D(filters=ff_dim, kernel_size=1, activation="relu")(res)
    x = layers.Dropout(dropout)(x)
    x = layers.Conv1D(filters=inputs.shape[-1], kernel_size=1)(x)
    x = layers.LayerNormalization(epsilon=1e-6)(x)
    return x + res

inputs = layers.Input(shape=(X.shape[1], X.shape[2]))
x = transformer_encoder(inputs, head_size=64, num_heads=4, ff_dim=4, dropout=0.1)
x = layers.GlobalAveragePooling1D(data_format="channels_last")(x)
x = layers.Dense(20, activation="relu")(x)
outputs = layers.Dense(1)(x)

model = models.Model(inputs, outputs)
model.compile(optimizer="adam", loss="mse")

print("🤖 The Transformer is deep-thinking... this is harder than the LSTM...")
model.fit(X, y, epochs=10, batch_size=32)

# 4. Save the Genius
model.save("transformer_detective.keras")
print("🎉 SUCCESS: 'transformer_detective.keras' is ready!")