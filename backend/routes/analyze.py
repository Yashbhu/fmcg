# backend/routes/analyze.py
from fastapi import APIRouter
from model.technical_agent_logic import analyze_rfp_specs
from model.pricing_agent_logic import calculate_pricing
from model.sales_agent_logic import scrape_all_tenders

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/run")
def run_analysis():
    """Run technical + pricing analysis on scraped tenders."""
    rfp = scrape_all_tenders()
    if not rfp:
        return {"status": "no_tenders_found"}
    
    technical = analyze_rfp_specs(rfp)
    if technical is None:
        return {"status": "technical_analysis_failed"}
    
    pricing = calculate_pricing(technical)
    if pricing is None:
        return {"status": "pricing_failed"}
    
    return {
        "status": "completed",
        "technical": technical.to_dict(orient="records"),
        "pricing": pricing.to_dict(orient="records"),
    }
