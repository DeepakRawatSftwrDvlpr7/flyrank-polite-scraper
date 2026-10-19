# The Polite Scraper (FlyRank BE-05)

A polite web scraper that extracts 60 books from `books.toscrape.com`, transforms messy HTML into clean data, and validates it against a strict schema.

## Features
- **Polite:** Uses a custom `User-Agent` identifying the bot and uses `time.sleep(2)` to avoid overwhelming the server.
- **Robust:** Uses `try-except` blocks around network requests to survive broken pages without crashing.
- **Data Validation:** Uses `Pydantic` to ensure prices are cleaned (removing the £ symbol) and parsed as real `float` numbers before saving.
- **Output:** Saves the cleaned dataset to `books.json`.

## Run Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run the scraper: `python scraper.py`
3. Check the generated `books.json` file to view the structured data.
