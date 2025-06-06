import pandas as pd
from scraper import scrape_books_from_page
from config import BASE_URL,MONGO_URI
from pymongo import MongoClient
from datetime import datetime,timezone
# Connect to MongoDB Atlas

client = MongoClient(MONGO_URI)
db = client["bookstore"]
collection = db["books"]

def save_to_mongo(data):
    inserted_count = 0
    for book in data:
        # Add timestamp
        book["scraped_at"] = datetime.now(timezone.utc)

        # Check for duplicate using Product URL
        if not collection.find_one({"Product URL": book["Product URL"]}):
            collection.insert_one(book)
            inserted_count += 1

    print(f"{inserted_count} new records saved to MongoDB.")

def main():
    all_books = []

    url = BASE_URL + "page-1.html"
    print(f"Scraping {url}...")
    books = scrape_books_from_page(url)
    all_books.extend(books)

    save_to_mongo(all_books)

    # Optional: Save to CSV too
    df = pd.DataFrame(all_books)
    df.to_csv("data/book_details.csv", index=False)
    print("Scraping complete! Saved to MongoDB and CSV.")

if __name__ == "__main__":
    main()
