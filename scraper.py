import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError
import time
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Stage: Define Schema for clean data
class Book(BaseModel):
    title: str
    price: float
    in_stock: bool

def scrape_books(pages_to_scrape=3):
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    
    # Stage: Politeness - Say who you are
    headers = {
        "User-Agent": "FlyRank-PoliteScraper/1.0 (Learning Project; contact: amssre.17286@gmail.com)"
    }
    
    all_books = []

    for page in range(1, pages_to_scrape + 1):
        url = base_url.format(page)
        logging.info(f"Scraping {url}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Check for broken pages (404, 500)
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve page {page}: {e}")
            continue  # Survive a broken page without crashing

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            try:
                # Extract messy data
                title = book.h3.a["title"]
                
                raw_price = book.find("p", class_="price_color").text
                # Clean price (e.g., "£51.77" -> 51.77)
                clean_price = float(raw_price.replace("Â£", "").replace("£", "").strip())
                
                raw_stock = book.find("p", class_="instock availability").text.strip()
                in_stock = "in stock" in raw_stock.lower()

                # Validate with Pydantic Schema
                valid_book = Book(title=title, price=clean_price, in_stock=in_stock)
                all_books.append(valid_book.model_dump())
            
            except (AttributeError, ValueError, ValidationError) as e:
                logging.warning(f"Skipping a book due to parsing/validation error: {e}")
                continue

        # Stage: Politeness - Go slowly
        time.sleep(2)

    # Save to JSON
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(all_books, f, indent=4, ensure_ascii=False)
    
    logging.info(f"Successfully scraped and saved {len(all_books)} books to books.json")

if __name__ == "__main__":
    scrape_books(3)
