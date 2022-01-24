import requests
from typing import Dict, Any
from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urlparse
import urllib.request
import os.path


# Creates get_data function and use requests module to access URL
# content and transform it into text object decoded by utf-8
def _get_data(url):
    """
    :param url: Give the Book to scrap website url
    :return: Beautifulsoup item parsed as HTML and decoded by utf-8
    """
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data.decode('utf-8'), features="html.parser")
    return soup


def _get_rating(soup: BeautifulSoup) -> int:
    """
    :param soup: Give the Beautifulsoup item previously created
    :return: finds the star_rating element of the book, return an integer based on what is contained in the star_rating
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
    :param soup: Give the Beautifulsoup item previously created
    :return: Finds the Book title, return The Book title as text
    """
    title = soup.find('h1').get_text()
    return title


def _get_category(soup: BeautifulSoup):
    """
    :param soup: Give the Beautifulsoup item previously created,
    :return  Finds the "breadcrumb" element and select the 3rd 'a'
    occurrence, return the Book category name
    """
    book_breadcrumb = soup.find(class_='breadcrumb')
    if book_breadcrumb is not None:
        book_items = book_breadcrumb.find_all('a')
        category_content = book_items[2].get_text()
        return category_content


def _get_table_value(soup: BeautifulSoup, header_name: str):
    """
    :param soup: Give the Beautifulsoup item previously created
    :param header_name: Give the name of the researched item inside the table (example "UPC" or "Price (excl. tax)"
    :return: The value linked to the given header_name
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
    :param soup: Give the Beautifulsoup item previously created
    :return: Only the first 'p' tag occurrence, return the description as text if it exists
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
    :param soup: Give the Beautifulsoup item previously created
    :return: Find the book's image and the incomplete image's link, restructures the image's link and name properly,
    saves the image into a file named by the Book's name and return the image complete url
    """
    web_url = 'https://books.toscrape.com/'
    category_name = _get_category(soup)
    for item in soup.find_all('img'):
        image = (item['src'])
        image_name = (item['alt'])
        new_image_name_1 = [element for element in image_name if element != ':']
        new_image_name_2 = [element for element in new_image_name_1 if element != '/']
        new_image_name_3 = [element for element in new_image_name_2 if element != ' ']
        new_image_name_4 = [element for element in new_image_name_3 if element != '"']
        final_image_name = ''.join(new_image_name_4) + '.jpg'
        image_link = urlparse(image)
        image_object = image_link.path
        new_path = image_object.split('/')
        final_path = [element for element in new_path if element != '..']
        final_url = web_url + final_path[0] + '/' + final_path[1] + '/' + final_path[2] + '/' + final_path[3] + '/' + final_path[4]
        saving_path = os.path.join(category_name)
        if not os.path.isdir(saving_path):
            os.makedirs(saving_path)
        os.chdir(saving_path)
        urllib.request.urlretrieve(final_url, final_image_name)
        os.chdir('..')
        return final_url


def scrap_book_url(url: str) -> Dict[str, Any]:
    """
    :param url: Give the desired Book url
    :return: A dictionary with all the book keys and values
    """
    book_url = url
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
    book_features = {'book_url': book_url, 'title': book_title, 'category': book_category,
                     'description': book_description,
                     'image link': book_image, 'upc': upc, 'price excluding taxes': price_excl_tva,
                     'prince including taxes': price_incl_tva,
                     'in stock availability': stock, 'star rating': rating}
    return book_features
