import psycopg2
import pandas as pd

# 1. Connect to the Filing Cabinet
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres123",
    host="localhost"
)

print("Reading data from database...")

# 2. Pull the data into a Pandas Table (DataFrame)
query = "SELECT * FROM raw_transactions"
df = pd.read_sql(query, conn)

print(f"Total rows collected: {len(df)}")

# 3. CLEANING: Remove 0.0 ETH transactions (they are just smart contract calls)
df_clean = df[df['eth_value'] > 0].copy()

# 4. FEATURE ENGINEERING: Calculate 'Gas in Gwei' (Easier for AI to read)
df_clean['gas_gwei'] = df_clean['gas_price'] / 10**9

# 5. FEATURE ENGINEERING: Time Difference (How many seconds between transactions)
df_clean = df_clean.sort_values(f'timestamp')
df_clean['time_diff'] = df_clean['timestamp'].diff().dt.total_seconds().fillna(0)

print(f"Rows after cleaning: {len(df_clean)}")

# 6. SAVE AS CSV (This is the food for our AI)
df_clean.to_csv("cleaned_data.csv", index=False)

print("🎉 SUCCESS: 'cleaned_data.csv' is ready for the Transformer!")

conn.close()