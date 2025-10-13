# technical_agent_logic.py
import pandas as pd
from groq import Groq
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

# --- SETUP GROQ API CLIENT ---
try:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Groq API key not found. Please set the GROQ_API_KEY in your .env file.")
    client = Groq(api_key=api_key)
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

# --- Using the correct and available model name ---
ACTIVE_MODEL = "llama-3.1-8b-instant"

RFP_DOCUMENT_TEXT = """
Technical Scope of Supply for Delhi Metro Phase V:
The contractor shall supply, install, test, and commission the following 1.1 kV grade power cables.
Item 1: Armored Power Cable with specs: Voltage Rating 1.1 kV, Conductor Material Copper, Insulation Type XLPE, Armor Type Steel Wire.
Item 2: Armored Power Cable with specs: Voltage Rating 1.1 kV, Conductor Material Aluminium, Insulation Type XLPE, Armor Type Steel Wire.
"""

def analyze_rfp_specs(rfp_summary):
    """
    Analyzes RFP text using the correct Groq Llama3 model.
    """
    print(f"⚙️  Technical Agent (Groq): Starting analysis with model {ACTIVE_MODEL}...")
    if not client:
        return None

    prompt = f"""
    From the RFP text below, extract technical specs for each item into a clean JSON array.
    The keys must be "VoltageRating", "ConductorMaterial", "InsulationType", "ArmorType".
    Your response must ONLY be the JSON array inside a ```json code block.

    RFP Text: --- {RFP_DOCUMENT_TEXT} ---
    """
    try:
        response = client.chat.completions.create(
            model=ACTIVE_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        # We need a more flexible regex for the new model's output
        json_text_match = re.search(r'```json\n(.*?)\n```', response.choices[0].message.content, re.DOTALL)
        if not json_text_match:
             raise ValueError("Could not find a JSON block in the model's response.")
        
        json_text = json_text_match.group(1)
        required_products = json.loads(json_text)
        print("   - Step 1.2: Successfully extracted specs via Groq.")
    except Exception as e:
        print(f"❗️ ERROR (Technical Agent): Failed to get valid response from Groq. Error: {e}")
        return None

    try:
        oem_products_df = pd.read_csv('product_database.csv')
    except FileNotFoundError:
        print("   - ❗️ ERROR: product_database.csv not found!")
        return None

    final_recommendations = []
    for i, req_product in enumerate(required_products):
        req_specs = {k: str(v).strip() for k, v in req_product.items()}
        scores = []
        for index, oem_product in oem_products_df.iterrows():
            matched_specs = sum(1 for key, val in req_specs.items() if str(oem_product.get(key, '')).strip() == val)
            score = (matched_specs / len(req_specs)) * 100
            scores.append({'SKU': oem_product['SKU'], 'Score': score})
        
        best_match = sorted(scores, key=lambda x: x['Score'], reverse=True)[0]
        final_recommendations.append({
            'RFP_Item': f"Item {i+1}", 
            'Recommended_SKU': best_match['SKU'], 
            'Match_Score': best_match['Score']
        })

    final_df = pd.DataFrame(final_recommendations)
    print("✅ Technical Agent: Analysis complete.")
    return final_df