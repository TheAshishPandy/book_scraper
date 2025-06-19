from scraper import scrape_books_from_page
from config import BASE_URL, CATEGORY_SLUGS, MONGO_URI
from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timezone
import certifi
import os

def get_mongo_client():
    """Create a secure MongoDB client with SSL/TLS support"""
    return MongoClient(
        MONGO_URI,
        tlsCAFile=certifi.where(),
        connectTimeoutMS=30000,
        socketTimeoutMS=30000,
        serverSelectionTimeoutMS=30000
    )

def save_to_mongo(data):
    new_count = 0
    try:
        client = get_mongo_client()
        collection = client["bookstore"]["books"]
        
        for book in data:
            book["scraped_at"] = datetime.now(timezone.utc)
            if not collection.find_one({"Product URL": book["Product URL"]}):
                collection.insert_one(book)
                new_count += 1
        print(f"{new_count} new records saved to MongoDB.")
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
    finally:
        client.close()

def main():
    all_books = []

    for category_name, slug in CATEGORY_SLUGS.items():
        url = f"{BASE_URL}category/books/{slug}/index.html"
        print(f"Scraping category {category_name!r} at {url}")
        books = scrape_books_from_page(url)
        for book in books:
            book["Category"] = category_name
        all_books.extend(books)

    save_to_mongo(all_books)

    # Optional CSV export
    df = pd.DataFrame(all_books)
    df.to_csv("data/book_details.csv", index=False)
    print("Done! Data saved to MongoDB and CSV.")

if __name__ == "__main__":
    main()