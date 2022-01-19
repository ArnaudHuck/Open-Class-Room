import requests
from typing import Dict, List
from bs4 import BeautifulSoup
from Book_Scraper import scrap_book_url
from urllib.parse import urlparse


def join_category_url(url: str):
    """
    :param url: Give a book url from the scraped category page
    :return: parse the path of the given url, and adds the global website's url
    return usable book url
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
    :param url:give a book url from the scraped home page
    :return: add new path to the given url
    return usable url
    """
    web_url = 'https://books.toscrape.com/catalogue/'
    new_url = web_url + url
    return new_url


def _get_data(url):
    """
    :param url: give a url
    :return: return the text from the html object
    """
    r = requests.get(url)
    return r.text


def scrap_page_books_category(page_url: str) -> List[Dict]:
    """
    :param page_url: give a category page url
    :return: Changes the url into a Beautifulsoup item, finds all books urls on the page,
    scrap all the element previously modified
    return a list of dictionaries holding all the category's page
    """
    soup = BeautifulSoup(_get_data(page_url), 'html.parser')
    book_library = soup.find_all("article", {"class": "product_pod"})
    book_urls = [book.find("a")["href"] for book in book_library]
    dict_list = [scrap_book_url(join_category_url(url)) for url in book_urls]
    return dict_list


def scrap_page_books_global(page_url: str) -> List[Dict]:
    """
    :param page_url: give the 'https://books.toscrape.com/catalogue/page-1.html' url
    :return: Changes the given url into a Beautiful item, finds all books urls on the page,
    scrap all the element previously modified
    return a list of dictionaries holding all the books' information from the page
    """
    soup = BeautifulSoup(_get_data(page_url), 'html.parser')
    book_library = soup.find_all("article", {"class": "product_pod"})
    book_urls = [book.find("a")["href"] for book in book_library]
    dict_list = [scrap_book_url(join_global_url(url)) for url in book_urls]
    return dict_list
