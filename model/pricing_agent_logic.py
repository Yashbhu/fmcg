# pricing_agent_logic.py
import pandas as pd

def calculate_pricing(technical_analysis_df):
    """
    Calculates pricing based on the technical analysis, product prices,
    and testing costs.
    """
    print("💰 Pricing Agent: Starting cost calculation...")
    
    if technical_analysis_df is None or technical_analysis_df.empty:
        print("❗️ ERROR (Pricing Agent): No technical analysis provided to calculate pricing.")
        return None
        
    try:
        product_prices_df = pd.read_csv('product_prices.csv')
        test_prices_df = pd.read_csv('test_prices.csv')
    except FileNotFoundError as e:
        print(f"❗️ ERROR (Pricing Agent): Missing data file - {e}")
        return None
    
    # Merge the technical recommendations with the product price list
    pricing_df = pd.merge(
        technical_analysis_df, 
        product_prices_df, 
        left_on='Recommended_SKU', 
        right_on='SKU', 
        how='left'
    )
    
    # For this project, we assume all tests are required for the RFP
    total_test_cost = test_prices_df['TestCost'].sum()
    pricing_df['Test_Cost'] = total_test_cost
    
    # Calculate the final total cost per item
    pricing_df['Total_Cost'] = pricing_df['UnitPrice'] + pricing_df['Test_Cost']
    
    print("✅ Pricing Agent: Calculation complete.")
    return pricing_df