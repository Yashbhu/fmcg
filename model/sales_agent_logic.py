# sales_agent_logic.py
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scan_and_select_rfp(html_file_path):
    """
    Scans a local HTML file for RFPs and selects one that is due
    within the next 3 months from a fixed demo date.
    """
    print("🤖 Sales Agent: Scanning for new RFPs...")
    
    # We use a fixed date for this example to ensure the output is consistent.
    # In a real application, you would use datetime.now().
    now = datetime(2025, 10, 13) 
    cutoff_date = now + timedelta(days=90)
    
    with open(html_file_path, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    for item in soup.find_all('div', class_='rfp-item'):
        try:
            due_date_str = item.find('span', class_='due-date').text
            rfp_due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            
            # The core logic: Is the due date in the future but before our cutoff?
            if now < rfp_due_date <= cutoff_date:
                selected_rfp = {
                    "title": item.find('h2').text.strip(),
                    "due_date": due_date_str
                }
                print(f"🏆 Sales Agent: Selected RFP '{selected_rfp['title']}'")
                return selected_rfp
        except (AttributeError, ValueError):
            # Handles cases where an RFP item might be malformed or missing a date
            continue
            
    print("😔 Sales Agent: No suitable RFPs found.")
    return None