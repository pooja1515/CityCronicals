import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import warnings
import logging

warnings.filterwarnings('ignore')

# -------------------- CONFIGURATION --------------------
CHROME_DRIVER_PATH = r'C:\Users\Ayush\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
CITY_NAME = "ahmedabad"
BASE_URL = f"https://english.gujaratsamachar.com/city/{CITY_NAME}"
HEADERS = {"User-Agent": "Mozilla/5.0"}
MAX_ARTICLES = float("inf")  # Set to float('inf') to scrape all articles
DAYS_TO_SCRAPE = 184
CHECKPOINT_EVERY = 10  # Save a checkpoint every N articles
CHECKPOINT_PATH = f"news_articles_{CITY_NAME}_checkpoint.csv"
FINAL_OUTPUT_PATH = f"news_articles_{CITY_NAME}.csv"

# -------------------- LOGGER SETUP --------------------
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# -------------------- SETUP SELENIUM OPTIONS --------------------
def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    service = Service(executable_path=CHROME_DRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

# -------------------- FETCH ARTICLE CONTENT USING SELENIUM --------------------
def fetch_article_content(url):
    driver = get_chrome_driver()
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html

# -------------------- PARSE AND EXTRACT ARTICLE DETAILS --------------------
def parse_article_page(html):
    soup = BeautifulSoup(html, 'html.parser')

    article_div = soup.find('div', class_='article')
    article_text = article_div.get_text(separator=' ', strip=True) if article_div else ""

    updated_date = None
    date_p = soup.find('p', class_='text-muted mb-0')
    if date_p:
        date_text = date_p.get_text(strip=True)
        date_match = re.search(r'Updated:\s+([A-Za-z]+)\s+(\d{1,2})[a-z]{2},\s+(\d{4})', date_text)
        if date_match:
            month_str = date_match.group(1)
            day = int(date_match.group(2))
            year = int(date_match.group(3))
            month_num = datetime.strptime(month_str, "%b").month
            updated_date = f"{year}-{month_num:02d}-{day:02d}"

    return article_text, updated_date

# -------------------- SAVE CHECKPOINT --------------------
def save_checkpoint(data, path):
    pd.DataFrame(data).to_csv(path, index=False)
    logging.info(f"💾 Checkpoint saved with {len(data['Title'])} articles to '{path}'")

# -------------------- SCRAPE ARTICLES BY DATE --------------------
def scrape_articles():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=DAYS_TO_SCRAPE)
    date_range = pd.date_range(start=start_date, end=end_date)

    data = {
        "Title": [], "Article Link": [], "Date": [], "Day": [],
        "Month": [], "Year": [], "Article": [], "Location": []
    }

    for current_date in tqdm(date_range, desc="Scraping by date"):
        if len(data["Title"]) >= MAX_ARTICLES:
            break

        formatted_date = current_date.strftime('%Y-%m-%d')
        page = 1

        while True:
            if len(data["Title"]) >= MAX_ARTICLES:
                break

            url = f"{BASE_URL}/{page}?date={formatted_date}"
            response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all('a')
            found_any = False

            for link in links:
                if len(data["Title"]) >= MAX_ARTICLES:
                    break

                title = link.get('title')
                href = link.get('href')
                if title and href and title not in data["Title"]:
                    full_link = f"https://english.gujaratsamachar.com{href}"
                    article_html = fetch_article_content(full_link)
                    article_text, extracted_date = parse_article_page(article_html)

                    if not article_text:
                        continue

                    date_to_use = extracted_date or formatted_date
                    date_obj = datetime.strptime(date_to_use, "%Y-%m-%d")

                    data["Title"].append(title)
                    data["Article Link"].append(full_link)
                    data["Date"].append(date_to_use)
                    data["Day"].append(date_obj.day)
                    data["Month"].append(f"{date_obj.month:02d}")
                    data["Year"].append(date_obj.year)
                    data["Article"].append(article_text)
                    data["Location"].append(CITY_NAME)

                    logging.info(f"📰 Scraped: {title}")

                    found_any = True

                    # Checkpoint save
                    if len(data["Title"]) % CHECKPOINT_EVERY == 0:
                        save_checkpoint(data, CHECKPOINT_PATH)

            if not found_any:
                break

            page += 1

    return pd.DataFrame(data)

# -------------------- MAIN EXECUTION --------------------
if __name__ == "__main__":
    logging.info("🚀 Starting article scraping...")
    df = scrape_articles()
    df.to_csv(FINAL_OUTPUT_PATH, index=False)
    logging.info(f"\n✅ All done! Final dataset saved to '{FINAL_OUTPUT_PATH}'")
