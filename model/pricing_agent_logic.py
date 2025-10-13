import pandas as pd
import sqlite3
import os
import numpy as np

def calculate_pricing(technical_analysis_df: pd.DataFrame):
    """
    Calculates total pricing based on matched SKUs from the Technical Agent.
    Pulls price data and test costs from the SQLite database.
    Returns a final DataFrame including total costs.
    """
    print("💰 Pricing Agent: Starting cost calculation...")

    # --- Step 0: Validate input ---
    if technical_analysis_df is None or technical_analysis_df.empty:
        print("❗️ ERROR: No technical analysis data provided to Pricing Agent.")
        return None

    # --- Step 1: Connect to database ---
    DB_PATH = "rfp_database.db"
    if not os.path.exists(DB_PATH):
        print(f"⚠️ Database not found: {DB_PATH}")
        print("👉 Please run `python model/init_db_pricing.py` to initialize it.")
        return None

    try:
        conn = sqlite3.connect(DB_PATH)
        product_prices_df = pd.read_sql_query("SELECT SKU, UnitPrice FROM products", conn)
        test_prices_df = pd.read_sql_query("SELECT TestName, TestCost FROM tests", conn)
        conn.close()
    except sqlite3.Error as e:
        print(f"❗️ Database read error: {e}")
        return None

    # --- Step 2: Merge technical matches with product prices ---
    merged_df = pd.merge(
        technical_analysis_df,
        product_prices_df,
        left_on="Recommended_SKU",
        right_on="SKU",
        how="left"
    )

    # --- Step 3: Calculate total cost ---
    if "UnitPrice" not in merged_df.columns:
        print("❗️ Missing UnitPrice column in products table.")
        return None

    total_test_cost = test_prices_df["TestCost"].sum() if not test_prices_df.empty else 0
    merged_df["Test_Cost"] = total_test_cost
    merged_df["Total_Cost"] = merged_df["UnitPrice"].fillna(0) + merged_df["Test_Cost"]

    # --- Step 4: Clean data (avoid NaN/inf errors when converting to JSON) ---
    merged_df.replace([np.inf, -np.inf], 0, inplace=True)
    merged_df.fillna(0, inplace=True)

    # --- Step 5: Display summary ---
    print(f"✅ Pricing Agent: Completed pricing for {len(merged_df)} items.")
    print("🧾 Total Test Cost Applied (Flat):", total_test_cost)

    # --- Step 6: Return cleaned DataFrame ---
    return merged_df
