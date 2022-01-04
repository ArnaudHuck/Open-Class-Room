import requests
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
from scrap_page_url import



def scrap_category_books(url: str) -> List[Dict]:
    all_books = scrap_page_books_category(url)
    next_url = url
    while next_page_url(next_url) is not None:
        next_url = next_page_url(url)
        next_page = scrap_page_books_category(next_url)
        all_books.extend(next_page)
    return all_books