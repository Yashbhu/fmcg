import sqlite3
import pandas as pd

DB_PATH = "rfp_database.db"
conn = sqlite3.connect(DB_PATH)

# --- Create Products Table ---
conn.execute("""
CREATE TABLE IF NOT EXISTS products (
    SKU TEXT PRIMARY KEY,
    ProductName TEXT,
    Category TEXT,
    UnitPrice REAL
)
""")

# --- Create Tests Table ---
conn.execute("""
CREATE TABLE IF NOT EXISTS tests (
    TestName TEXT PRIMARY KEY,
    TestCost REAL
)
""")

# --- Insert Sample Data ---
product_data = [
    ("SKU001", "Dell PowerEdge R740", "Server", 1200.0),
    ("SKU002", "HP ProLiant DL380", "Server", 1300.0),
    ("SKU003", "Lenovo ThinkSystem SR650", "Server", 1100.0)
]

test_data = [
    ("Load Test", 200.0),
    ("Performance Test", 300.0),
    ("Compliance Test", 150.0)
]

pd.DataFrame(product_data, columns=["SKU", "ProductName", "Category", "UnitPrice"]).to_sql(
    "products", conn, if_exists="replace", index=False
)

pd.DataFrame(test_data, columns=["TestName", "TestCost"]).to_sql(
    "tests", conn, if_exists="replace", index=False
)

conn.close()
print("✅ Pricing database initialized successfully with sample data!")
