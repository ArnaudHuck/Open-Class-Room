import requests
from typing import Dict, Any
from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urlparse
import urllib.request


# Creates get_data function and use requests module to access URL
# content and transform it into text object decoded by utf-8
def _get_data(url):
    """
    :param url:
    :return:
    """
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data.decode('utf-8'), features="html.parser")
    return soup


def _get_book_url(soup: BeautifulSoup):
    """
    :param soup:
    :return:
    """
    books = soup.find("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    for elements in books:
        book_url = elements.find("href")
        print(book_url)
        pass


def _get_rating(soup: BeautifulSoup) -> int:
    """
    :param soup:
    :return:
    """
    star_rating_tag = soup.find("p", {"class": "star-rating"})
    star_rating_class = star_rating_tag["class"]
    rating_class_name = star_rating_class[1]
    if rating_class_name == "One":
        return 1
    elif rating_class_name == "Two":
        return 2
    elif rating_class_name == "Three":
        return 3
    elif rating_class_name == "Four":
        return 4
    elif rating_class_name == "Five":
        return 5


def _get_title(soup: BeautifulSoup):
    """
    :param soup:
    :return:
    """
    title = soup.find('h1').get_text()
    return title


def _get_category(soup: BeautifulSoup):
    """
    :param soup:
    :return:
    """
    book_breadcrumb = soup.find(class_='breadcrumb')
    if book_breadcrumb is not None:
        book_items = book_breadcrumb.find_all('a')
        category_content = book_items[2].get_text()
        return category_content


def _get_table_value(soup: BeautifulSoup, header_name: str):
    """
    :param soup:
    :param header_name:
    :return:
    """
    table = soup.find(class_="table")
    table_elements = table.find_all('tr')
    for element in table_elements:
        header = element.find('th')
        cells = element.find('td')
        if (header.contents[0]) == header_name:
            header_name = cells.contents[0]
            return header_name


def _get_description(soup: BeautifulSoup):
    """
    :param soup:
    :return:
    """
    book_para = soup.find(class_="product_page")
    description = book_para.find('p', recursive=False)
    if description is None:
        description = ''
    else:
        description = description.get_text()
    return description


def _get_img(soup: BeautifulSoup):
    """
    :param soup:
    :return:
    """
    web_url = 'https://books.toscrape.com/'
    for item in soup.find_all('img'):
        image = (item['src'])
        image_link = urlparse(image)
        path = image_link.path
        new_path = path.split('/')
        final_path = [element for element in new_path if element != '..']
        final_url = web_url + final_path[0] + '/' + final_path[1] + '/' + final_path[2] + '/'+ final_path[3] + '/' + final_path[4]
        urllib.request.urlretrieve(final_url, (item['alt'] + '.jpg'))
        return final_url


def scrap_book_url(url: str) -> Dict[str, Any]:
    """
    :param url:
    :return:
    """
    book_soup = _get_data(url)
    book_title = _get_title(book_soup)
    book_category = _get_category(book_soup)
    book_description = _get_description(book_soup)
    book_image = _get_img(book_soup)
    upc = _get_table_value(book_soup, 'UPC')
    price_excl_tva = _get_table_value(book_soup, 'Price (excl. tax)')
    price_incl_tva = _get_table_value(book_soup, 'Price (incl. tax)')
    stock = _get_table_value(book_soup, 'Availability')[10:12]
    rating = _get_rating(book_soup)
    book_features = {'title': book_title, 'category': book_category, 'description': book_description,
                     'image link': book_image, 'upc': upc, 'price excluding taxes': price_excl_tva,
                     'prince including taxes': price_incl_tva,
                     'in stock availability': stock, 'star rating': rating}
    return book_features

