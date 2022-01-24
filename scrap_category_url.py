import requests
import csv
from typing import List, Tuple, Dict
from bs4 import BeautifulSoup
from scrap_page_url import scrap_page_books_category


def _get_data(url: str):
    """
    :param url: give a url
    :return: return the text from the response object
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


def get_category_urls(url: str) -> List[Tuple[str, str]]:
    """
    :param url:
    :return:
    """
    soup = BeautifulSoup(_get_data(url), 'html.parser')
    side_categories = soup.find("ul", {"class": "nav nav-list"})
    category_list = side_categories.find_all("li")
    category_urls = ['https://books.toscrape.com/' + item.find("a")["href"] for item in category_list]
    category_name = [get_category_name_out(item) for item in category_list]
    category_urls.pop(0)
    category_name.pop(0)
    category_tuple = list(zip(category_urls, category_name))
    return category_tuple


def next_page_url(url: str):
    """
    :param url: Give a page url
    :return: Changes the url into a Beautifulsoup item, finds if a next page exists
    return None if it doesn't
    return the next page url previously modified
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
    :param url: Give a chosen category page url
    :return: Create a list of dictionaries from the first page, finds if a next page exists,
    if yes it scraps the next page and add the list of dictionaries to the existing one
    """
    all_books = scrap_page_books_category(url)
    next_url = url
    while next_page_url(next_url) is not None:
        next_url = next_page_url(next_url)
        next_page = scrap_page_books_category(next_url)
        all_books.extend(next_page)
    return all_books


def export_list_to_csv(dict_list: List[Dict], file_name: str):
    keys = dict_list[0].keys()
    with open(file_name, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)


def export_single_book_to_csv(dict_list: [Dict], file_name: str):
    field_names = ([k for k in dict_list])
    with open(file_name, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, field_names)
        dict_writer.writeheader()
        dict_writer.writerow(dict_list)