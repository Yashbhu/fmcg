from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import time

TENDER_SOURCES = {
    "eTenders (India Gov)": {
        "url": "https://etenders.gov.in/eprocure/app?page=FrontEndLatestActiveTenders&service=page",
        "table_selector": "table.list_table",
    },
    "GeM (Gov eMarketplace)": {
        "url": "https://bidplus.gem.gov.in/all-bids",
        "table_selector": "div.card-bid",
    },
}

def extract_etenders_tenders(soup):
    tenders = []
    table = soup.find("table", class_="list_table")
    if not table:
        print("⚠️ eTenders: table not found.")
        return tenders

    rows = table.find("tbody").find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue
        title = cols[1].text.strip()
        org = cols[2].text.strip()
        date_text = cols[3].text.strip()
        try:
            closing_date = datetime.strptime(date_text, "%d-%b-%Y %H:%M")
            tenders.append({
                "title": title,
                "organization": org,
                "closing_date": closing_date.strftime("%Y-%m-%d %H:%M"),
                "source": "eTenders"
            })
        except ValueError:
            continue
    return tenders


def extract_gem_tenders(soup):
    tenders = []
    cards = soup.find_all("div", class_="card-bid")
    if not cards:
        print("⚠️ GeM: no bid cards found.")
    for card in cards:
        title = card.find("h4").text.strip() if card.find("h4") else "N/A"
        org = card.find("p").text.strip() if card.find("p") else "N/A"
        date_text = "N/A"
        for span in card.find_all("span"):
            if "End Date" in span.text:
                date_text = span.text.split(":")[-1].strip()
        tenders.append({
            "title": title,
            "organization": org,
            "closing_date": date_text,
            "source": "GeM"
        })
    return tenders


def scrape_tenders():
    print("🚀 Sales Agent: Launching improved tender crawler...")
    all_tenders = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for site_name, config in TENDER_SOURCES.items():
            print(f"\n🌐 Scanning {site_name} ...")
            try:
                page.goto(config["url"], timeout=60000)
                page.wait_for_load_state("networkidle")
                time.sleep(5)

                # Optional screenshot for debugging
                page.screenshot(path=f"{site_name.replace(' ', '_')}.png")

                html = page.content()
                soup = BeautifulSoup(html, "html.parser")

                if "etenders" in config["url"]:
                    tenders = extract_etenders_tenders(soup)
                elif "gem.gov.in" in config["url"]:
                    tenders = extract_gem_tenders(soup)
                else:
                    tenders = []

                print(f"✅ {site_name}: Found {len(tenders)} tenders")
                all_tenders.extend(tenders)

            except Exception as e:
                print(f"❗ Error scraping {site_name}: {e}")
                continue

        browser.close()

    df = pd.DataFrame(all_tenders)
    if not df.empty:
        df.to_csv("tenders.csv", index=False)
        print(f"\n💾 Saved {len(df)} tenders to tenders.csv")
    else:
        print("\n😔 No tenders found. Try increasing wait time or check screenshots.")

    return df


if __name__ == "__main__":
    result_df = scrape_tenders()
    print("\n📊 Preview:")
    print(result_df.head() if not result_df.empty else "No tenders found.")
