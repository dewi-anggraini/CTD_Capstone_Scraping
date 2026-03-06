# 1. Web Scraping Program

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import pandas as pd 
import time

# Step 1: Setup Scraper
driver = webdriver.Chrome()

# Step 1 (Optional): Configure browser options.
# Set acustom user-agent, if needed. So, the browser looks like a normal use.
#options = webdriver.ChromeOptions() 
#options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)") 
#driver = webdriver.Chrome(options=options)

# Step 2: Open MLB history page 
driver.get("https://www.baseball-almanac.com/yearmenu.shtml") 
time.sleep(3)

# Step 2: Collect year links 
year_links = driver.find_elements(By.TAG_NAME, "a")
year_urls = [(link.text.strip(), link.get_attribute("href")) 
             for link in year_links if link.text.strip().isdigit()] 

standings_data, batting_data, pitching_data = [], [], [] 

# Step 3: Visit each year page and scrape tables  
for year, url in year_urls[:3]: # limit to first 3 years
    driver.get(url) 
    # Wait until at least one table is present 
    WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.TAG_NAME, "table")) ) 
    
    # Find all tables on the page 
    tables = driver.find_elements(By.TAG_NAME, "table") 
    for table in tables: 
        rows = table.find_elements(By.TAG_NAME, "tr") 
        if len(rows)<2: continue

        # Try headers from <th>, fallback to <td> 
        header = [th.text.strip().lower() for th in rows[1].find_elements(By.TAG_NAME, "th")] 
        if not header: header = [td.text.strip().lower() 
                                 for td in rows[1].find_elements(By.TAG_NAME, "td")] 
        print("Year:", year, "Headers:", header) # debg
        
        # Standings 
        if any("team" in h for h in header) and any(h in ["w", "won"] for h in header):
            for row in rows[2:]: 
                cols = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")] 
                if cols: standings_data.append([year] + cols) 
        
        # Batting & Pitching 
        elif "statistic" in header and "name(s)" in header: 
            for row in rows[2:]: 
                cols = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")] 
                if cols: 
                    stat = cols[0].strip()
                    if "era" in stat: 
                        pitching_data.append([year] + cols) 
                    else: 
                        batting_data.append([year] + cols)

# Step 4: Save to CSV
pd.DataFrame(standings_data).to_csv("Standings.csv", index=False) 
pd.DataFrame(batting_data, columns=["Year","Statistic","Name(s)","Team(s)","#","Top 25"]).to_csv("BattingLeaders.csv", index=False)
pd.DataFrame(pitching_data, columns=["Year","Statistic","Name(s)","Team(s)","#","Top 25"]).to_csv("PitchingLeaders.csv", index=False)


# Step 5: Close browser 
driver.quit() 
print("Scraping complete! Data saved to mlb_history.csv")