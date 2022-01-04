import requests
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
from scrap_page_url import scrap_page_books_category
from scrap_page_url import scrap_page_books_global


def _get_data(url):
    """
    :param url:
    :return:
    """
    r = requests.get(url)
    return r.text


def get_category_name_out(item: str):
    """
    :param item:
    :return:
    """
    category_name = item.find('a').text.split('\n')[2].strip()
    return category_name


def get_category_urls(url: str) -> Tuple[list, list]:
    """
    :param url:
    :return:
    """
    soup = BeautifulSoup(_get_data(url), 'html.parser')
    side_categories = soup.find("ul", {"class": "nav nav-list"})
    category_list = side_categories.find_all("li")
    category_urls = [item.find("a")["href"] for item in category_list]
    category_name = [get_category_name_out(item) for item in category_list]
    category_urls.pop(0)
    category_name.pop(0)
    category_tuple = list(zip(category_urls, category_name))
    return category_tuple


def next_page_url(url: str):
    """
    :param url:
    :return:
    """
    soup = BeautifulSoup(_get_data(url), 'html.parser')
    pager = soup.find('li', {"class": 'next'})
    if pager is None:
        return None
    path = pager.find('a')["href"]
    new_url = '/'.join(url.split('/')[0: -1]) + '/' + path
    return new_url


def scrap_category_books(url: str) -> List[Dict]:
    """
    :param url:
    :return:
    """
    all_books = scrap_page_books_category(url)
    next_url = url
    while next_page_url(next_url) is not None:
        next_url = next_page_url(next_url)
        next_page = scrap_page_books_category(next_url)
        all_books.extend(next_page)
    return all_books


def scrap_home_books(url: str) -> List[Dict]:
    """
    :param url:
    :return:
    """
    all_books = scrap_page_books_global(url)
    next_url = url
    while next_page_url(next_url) is not None:
        next_url = next_page_url(next_url)
        next_page = scrap_page_books_global(next_url)
        all_books.extend(next_page)
    return all_books


def scrap_all_categories(url: str) -> List[Dict]:
    """
    :param url:
    :return:
    """
    category_tuple = get_category_urls(url)
    for category in category_tuple:
        print(scrap_category_books(category[0]))
    pass






