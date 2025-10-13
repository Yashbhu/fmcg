# pricing_agent_logic.py
import pandas as pd
import sqlite3

def calculate_pricing(technical_analysis_df):
    """
    Calculates pricing by reading product and test costs from the SQLite database.
    """
    print("💰 Pricing Agent: Starting cost calculation...")
    
    if technical_analysis_df is None or technical_analysis_df.empty:
        print("❗️ ERROR (Pricing Agent): No technical analysis provided to calculate pricing.")
        return None
        
    # --- Read from database instead of CSVs ---
    try:
        conn = sqlite3.connect('rfp_database.db')
        # Read both the products and tests tables
        product_prices_df = pd.read_sql_query("SELECT SKU, UnitPrice FROM products", conn)
        test_prices_df = pd.read_sql_query("SELECT * FROM tests", conn)
        conn.close()
    except sqlite3.Error as e:
        print(f"❗️ ERROR (Pricing Agent): Could not read from database. Error: {e}")
        return None
    # --- END OF MODIFICATION ---
    
    # Merge the technical recommendations with the product price list
    pricing_df = pd.merge(
        technical_analysis_df, 
        product_prices_df, 
        left_on='Recommended_SKU', 
        right_on='SKU', 
        how='left'
    )
    
    total_test_cost = test_prices_df['TestCost'].sum()
    pricing_df['Test_Cost'] = total_test_cost
    
    pricing_df['Total_Cost'] = pricing_df['UnitPrice'] + pricing_df['Test_Cost']
    
    print("✅ Pricing Agent: Calculation complete.")
    return pricing_df