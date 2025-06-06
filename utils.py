import requests 
from bs4 import BeautifulSoup
import time
import random

def get_soup(url):
    """Fetch the HTML content and return a BeautifulSoup object."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch {url} - {e}")
        return None

def clean_text(text):
    """Clean and normalize text."""
    return ' '.join(text.strip().split())

def get_rating(product):
    """Extract rating text from product HTML."""
    rating_map = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    try:
        classes = product.find('p', class_='star-rating')['class']
        for cls in classes:
            if cls in rating_map:
                return rating_map[cls]
        return 0
    except Exception:
        return 0

def sleep_random(min_sec=1, max_sec=3):
    """Sleep for a random interval to avoid being blocked."""
    time.sleep(random.uniform(min_sec, max_sec))

