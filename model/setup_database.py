import sqlite3
import pandas as pd


DB_FILE = "rfp_database.db"

def create_database():
    """Creates the SQLite database and populates it with initial data."""
    print("Creating and setting up the database...")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        SKU TEXT PRIMARY KEY,
        ProductName TEXT,
        VoltageRating TEXT,
        ConductorMaterial TEXT,
        InsulationType TEXT,
        ArmorType TEXT,
        UnitPrice REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tests (
        TestName TEXT PRIMARY KEY,
        TestCost REAL
    )
    """)
    print("Tables created successfully.")


    try:
 
        products_df = pd.read_csv('product_database.csv')
        prices_df = pd.read_csv('product_prices.csv')
        

        full_product_data = pd.merge(products_df, prices_df, on='SKU')
        

        full_product_data.to_sql('products', conn, if_exists='replace', index=False)
        print(f"{len(full_product_data)} products loaded into the database.")

 
        tests_df = pd.read_csv('test_prices.csv')
        tests_df.to_sql('tests', conn, if_exists='replace', index=False)
        print(f"{len(tests_df)} tests loaded into the database.")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find a required CSV file. {e}")
    finally:

        conn.commit()
        conn.close()
        print("Database setup complete.")

if __name__ == "__main__":
    create_database()
