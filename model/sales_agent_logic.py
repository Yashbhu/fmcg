# sales_agent_logic.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time
import os

# --- Multiple tender sources ---
TENDER_SOURCES = {
    "eTenders (India Gov)": {
        "url": "https://etenders.gov.in/eprocure/app?page=FrontEndLatestActiveTenders&service=page",
        "selector": "table.list_table",
        "type": "table",
    },
    "GeM (Gov eMarketplace)": {
        "url": "https://bidplus.gem.gov.in/all-bids",
        "selector": "div.card-bid, div.tender-card, div.bid-list-item",
        "type": "cards",
    },
}


# ----------------- ETENDERS SCRAPER -----------------
def extract_etenders_tenders(soup):
    """Extract tenders from eTenders.gov.in"""
    tenders = []
    table = soup.find("table", class_="list_table")
    if not table:
        print("⚠️ eTenders: table not found in page HTML.")
        return tenders

    tbody = table.find("tbody")
    if not tbody:
        print("⚠️ eTenders: no <tbody> found — page may have changed.")
        return tenders

    rows = tbody.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue
        title = cols[1].text.strip()
        org = cols[2].text.strip()
        date_text = cols[3].text.strip()

        try:
            closing_date = datetime.strptime(date_text, "%d-%b-%Y %H:%M")
        except ValueError:
            closing_date = None

        tenders.append({
            "title": title,
            "organization": org,
            "closing_date": closing_date.strftime("%Y-%m-%d %H:%M") if closing_date else date_text,
            "source": "eTenders"
        })

    return tenders


# ----------------- GEM SCRAPER -----------------
def extract_gem_tenders(soup):
    """Extract tenders from GeM bid portal."""
    tenders = []
    cards = soup.select("div.card-bid, div.tender-card, div.bid-list-item")

    if not cards:
        print("⚠️ GeM: No tender cards found. Structure might have changed.")
        return tenders

    for card in cards:
        title_tag = card.find(["h4", "h5", "a"])
        title = title_tag.text.strip() if title_tag else "N/A"

        org_tag = card.find("p")
        org = org_tag.text.strip() if org_tag else "N/A"

        date_text = "N/A"
        for span in card.find_all("span"):
            if "End Date" in span.text or "Bid End Date" in span.text:
                date_text = span.text.split(":")[-1].strip()

        tenders.append({
            "title": title,
            "organization": org,
            "closing_date": date_text,
            "source": "GeM"
        })

    return tenders


# ----------------- MAIN SCRAPER -----------------
def scrape_all_tenders():
    """
    Launches Playwright browser, scrapes multiple government tender sources,
    and returns a dataframe of tenders found.
    """
    print("🚀 Sales Agent: Launching multi-source tender crawler...")
    all_tenders = []

    with sync_playwright() as p:
        # 🟢 Run visibly (debug mode)
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()

        for site_name, config in TENDER_SOURCES.items():
            print(f"\n🌐 Scanning {site_name} ...")
            try:
                page.goto(config["url"], timeout=90000)
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(10000)  # wait for dynamic JS load

                screenshot_path = f"{site_name.replace(' ', '_')}.png"
                page.screenshot(path=screenshot_path)
                print(f"📸 Saved screenshot: {screenshot_path}")

                html = page.content()
                soup = BeautifulSoup(html, "html.parser")

                if config["type"] == "table":
                    tenders = extract_etenders_tenders(soup)
                elif config["type"] == "cards":
                    tenders = extract_gem_tenders(soup)
                else:
                    tenders = []

                print(f"✅ {site_name}: Found {len(tenders)} tenders.")
                all_tenders.extend(tenders)

            except Exception as e:
                print(f"❗ Error scraping {site_name}: {e}")
                continue

        browser.close()

    df = pd.DataFrame(all_tenders)
    if not df.empty:
        df.to_csv("tenders.csv", index=False)
        print(f"\n💾 Saved {len(df)} tenders to tenders.csv")

        selected_rfp = df.iloc[0].to_dict()
        print(f"\n🏆 Selected RFP: {selected_rfp['title']}")
        return selected_rfp
    else:
        print("\n😔 No tenders found. Check screenshots or increase wait time.")
        return None


# --- Standalone test run ---
if __name__ == "__main__":
    result = scrape_all_tenders()
    print("\n📊 Final Result:")
    print(result if result else "No tenders found.")
