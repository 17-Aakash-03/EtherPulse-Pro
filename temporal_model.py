import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 1. Load the cleaned food
df = pd.read_csv("cleaned_data.csv")
data = df[['eth_value', 'gas_gwei', 'time_diff']].values

# 2. Scale the numbers (AI hates big numbers, it likes numbers between 0 and 1)
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# 3. Create Sequences (Give the AI a 10-transaction memory)
X, y = [], []
for i in range(10, len(scaled_data)):
    X.append(scaled_data[i-10:i]) # The last 10 transactions
    y.append(scaled_data[i, 1])    # Try to predict the next Gas Price
X, y = np.array(X), np.array(y)

# 4. Build the Brain (The LSTM)
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
    LSTM(50),
    Dense(1) # One output: The predicted Gas Price
])

model.compile(optimizer='adam', loss='mean_squared_error')

print("🧠 The Brain is studying the data... please wait...")
model.fit(X, y, epochs=5, batch_size=32)

# 5. Save the Brain
model.save("gas_detective.h5")
print("🎉 SUCCESS: 'gas_detective.h5' brain is trained and saved!")