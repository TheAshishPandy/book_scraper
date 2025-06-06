import requests
from bs4 import BeautifulSoup
from config import BASE_URL, HEADERS
from utils import get_soup, clean_text, get_rating

def scrape_books_from_page(page_url):
    books = []
    soup = get_soup(page_url)
    if soup is None:
        return books

    product_list = soup.find_all('article', class_='product_pod')

    for product in product_list:
        title = product.h3.a['title']
        price = product.find('p', class_='price_color').text.strip()
        stock = product.find('p', class_='instock availability').text.strip()
        rating = get_rating(product)
        image_url = product.find('img')['src'].replace('../', 'http://books.toscrape.com/')
        product_relative_url = product.h3.a['href'].replace('../../../', '')
        product_url = BASE_URL + product_relative_url

        # Get author from the product page
        product_soup = get_soup(product_url)
        try:
            author = product_soup.find('div', class_='product_main').find_next('p').text.strip()
        except Exception:
            author = "N/A"

        books.append({
            'Title': title,
            'Author': author,
            'Price': price,
            'Stock': stock,
            'Rating': rating,
            'Image URL': image_url,
            'Product URL': product_url
        })

    return books
