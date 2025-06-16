from scraper import scrape_books_from_page
from config import BASE_URL, CATEGORY_SLUGS,MONGO_URI
from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timezone

client     = MongoClient(MONGO_URI)
collection = client["bookstore"]["books"]

def save_to_mongo(data):
    new_count = 0
    for book in data:
        book["scraped_at"] = datetime.now(timezone.utc)
        if not collection.find_one({"Product URL": book["Product URL"]}):
            collection.insert_one(book)
            new_count += 1
    print(f"{new_count} new records saved to MongoDB.")

def main():
    all_books = []

    for category_name, slug in CATEGORY_SLUGS.items():
        url = f"{BASE_URL}category/books/{slug}/index.html"
        print(f"Scraping category {category_name!r} at {url}")
        books = scrape_books_from_page(url)
        for book in books:
            book["Category"] =category_name;
        # 4. Collect
        all_books.extend(books)

    save_to_mongo(all_books)

    # Optional CSV export
    df = pd.DataFrame(all_books)
    df.to_csv("data/book_details.csv", index=False)
    print("Done! Data saved to MongoDB and CSV.")

if __name__ == "__main__":
    main()
