import psycopg2

# --- CONFIGURATION ---
# Change 'your_password' to the password you set when you installed Postgres
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres123", 
    "host": "localhost",
    "port": "5432"
}

def create_table():
    try:
        # 1. Connect to the database
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # 2. The SQL command to build the shelf
        sql_command = """
        CREATE TABLE IF NOT EXISTS raw_transactions (
            id SERIAL PRIMARY KEY,
            tx_hash TEXT UNIQUE,
            sender TEXT,
            receiver TEXT,
            eth_value NUMERIC,
            gas_price BIGINT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        # 3. Execute and Save
        cursor.execute(sql_command)
        conn.commit()
        
        print("🎉 SUCCESS: The table 'raw_transactions' is ready!")
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ ERROR: Could not connect to Postgres. Did you check your password?")
        print(f"Details: {e}")

if __name__ == "__main__":
    create_table()