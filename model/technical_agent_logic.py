# technical_agent_logic.py

import os
import re
import json
import time
import sqlite3
import pandas as pd
from dotenv import load_dotenv


try:
    from groq import Groq
except ImportError:
    Groq = None

load_dotenv()

client = None
api_key = os.getenv("GROQ_API_KEY")
if Groq and api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f" Error initializing Groq client: {e}")
else:
    print(" GROQ_API_KEY not set or Groq package missing — skipping live API mode.")

ACTIVE_MODEL = "llama-3.1-8b-instant"


RFP_DOCUMENT_TEXT = """
Technical Scope of Supply for Delhi Metro Phase V:
The contractor shall supply, install, test, and commission the following 1.1 kV grade power cables.
Item 1: Armored Power Cable — Voltage 1.1 kV, Conductor Copper, Insulation XLPE, Armor Steel Wire.
Item 2: Armored Power Cable — Voltage 1.1 kV, Conductor Aluminium, Insulation XLPE, Armor Steel Wire.
"""


def analyze_rfp_specs(rfp_summary: dict):
    """
    Extracts technical specs from an RFP (via Groq API) 
    and matches them to product SKUs from the SQLite database.
    Returns a DataFrame of recommended SKUs + scores.
    """
    print(" Technical Agent: Starting analysis...")


    rfp_text = ""
    if isinstance(rfp_summary, dict) and "title" in rfp_summary:
        rfp_text = rfp_summary["title"]
    elif isinstance(rfp_summary, str):
        rfp_text = rfp_summary
    else:
        rfp_text = RFP_DOCUMENT_TEXT


    prompt = f"""
    Extract all product technical specifications from this RFP text and return a JSON array.

    Required keys: "VoltageRating", "ConductorMaterial", "InsulationType", "ArmorType".
    Respond ONLY with a ```json code block.

    RFP Text:
    ---
    {rfp_text}
    ---
    """

    required_products = None


    if client:
        for i in range(3):
            try:
                response = client.chat.completions.create(
                    model=ACTIVE_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                )

                content = response.choices[0].message.content
                match = re.search(r"```json\s*(.*?)\s*```", content, re.DOTALL)
                if not match:
                    raise ValueError("No JSON block found in Groq response.")
                json_text = match.group(1)
                required_products = json.loads(json_text)
                print(" Extracted specs successfully from Groq.")
                break
            except Exception as e:
                print(f" Attempt {i+1} failed: {e}")
                time.sleep(2 ** i)
        else:
            print(" All attempts failed; using fallback specs.")
    else:
        print(" Skipping Groq API — using default RFP data.")
        required_products = [
            {
                "VoltageRating": "1.1 kV",
                "ConductorMaterial": "Copper",
                "InsulationType": "XLPE",
                "ArmorType": "Steel Wire",
            },
            {
                "VoltageRating": "1.1 kV",
                "ConductorMaterial": "Aluminium",
                "InsulationType": "XLPE",
                "ArmorType": "Steel Wire",
            },
        ]


    try:
        conn = sqlite3.connect("rfp_database.db")
        oem_df = pd.read_sql_query("SELECT * FROM products", conn)
        conn.close()
    except sqlite3.Error as e:
        print(f"Database read error: {e}")
        return None

    if not isinstance(required_products, list) or len(required_products) == 0:
        print(" No products extracted.")
        return None


    results = []
    for i, req in enumerate(required_products):
        req_clean = {k: str(v).strip().lower() for k, v in req.items()}
        best_match = {"SKU": None, "Score": 0}

        for _, row in oem_df.iterrows():
            matches = sum(
                1 for k, v in req_clean.items()
                if str(row.get(k, "")).strip().lower() == v
            )
            score = (matches / len(req_clean)) * 100
            if score > best_match["Score"]:
                best_match = {"SKU": row["SKU"], "Score": score}

        results.append({
            "RFP_Item": f"Item {i + 1}",
            "Recommended_SKU": best_match["SKU"],
            "Match_Score": best_match["Score"],
        })

    df = pd.DataFrame(results)
    print(" Technical Agent: Analysis complete.")
    return df

if __name__ == "__main__":
    print("🔍 Self-test: running analyze_rfp_specs() with sample RFP")
    print(analyze_rfp_specs({"title": RFP_DOCUMENT_TEXT}))
