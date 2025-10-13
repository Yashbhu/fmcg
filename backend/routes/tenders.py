# backend/routes/tenders.py
from fastapi import APIRouter
from model.sales_agent_logic import scrape_all_tenders

router = APIRouter(prefix="/tenders", tags=["Tenders"])

@router.get("/scrape")
def scrape_tenders():
    """Trigger tender scraping logic."""
    result = scrape_all_tenders()
    if result:
        return {"status": "success", "selected_rfp": result}
    return {"status": "no_tenders_found"}
