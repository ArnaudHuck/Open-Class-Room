import requests
from typing import Dict, List
from bs4 import BeautifulSoup
from Book_Scraper import scrap_book_url
from urllib.parse import urlparse


def join_category_url(url: str):
    """
    :param url:
    :return:
    """
    web_url = 'https://books.toscrape.com/catalogue/'
    new_url = urlparse(url)
    path = new_url.path
    new_path = path.split('/')
    final_path = [element for element in new_path if element != '..']
    final_url = web_url + final_path[0]
    return final_url


def join_global_url(url: str):
    """
    :param url:
    :return:
    """
    web_url = 'https://books.toscrape.com/catalogue/'
    new_url = web_url + url
    return new_url


def _get_data(url):
    """
    :param url:
    :return:
    """
    r = requests.get(url)
    return r.text


def scrap_page_books_category(page_url: str) -> List[Dict]:
    """
    :param page_url:
    :return:
    """
    soup = BeautifulSoup(_get_data(page_url), 'html.parser')
    book_library = soup.find_all("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    book_urls = [book.find("a")["href"] for book in book_library]
    dict_list = [scrap_book_url(join_category_url(url)) for url in book_urls]
    new_book_urls = [join_category_url(book) for book in book_urls]
    return dict_list


def scrap_page_books_global(page_url: str) -> List[Dict]:
    """
    :param page_url:
    :return:
    """
    soup = BeautifulSoup(_get_data(page_url), 'html.parser')
    book_library = soup.find_all("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    book_urls = [book.find("a")["href"] for book in book_library]
    dict_list = [scrap_book_url(join_global_url(url)) for url in book_urls]
    new_book_urls = [join_global_url(book) for book in book_urls]
    return dict_list
