import requests
from typing import Dict, List, Any
from bs4 import BeautifulSoup
import pandas as pd


# Creates get_data function and use requests module to access URL content and transform it into text object
def _get_data(url):
    r = requests.get(url)
    return r.text


library_page = _get_data('https://books.toscrape.com/index.html')
book_page = _get_data('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')
# Use BeautifulSoup module to transform Text object into soup object with html parser
book_soup = BeautifulSoup(book_page, 'html.parser')
library_soup = BeautifulSoup(library_page, 'html.parser')


def get_category_urls(soup: BeautifulSoup) -> List[str]:
    items = soup.find("aside", {"class": "sidebar col-sm-4 col-md-3"})
    category_list = items.find_all("li")
    category_urls = [item.find("a")["href"] for item in category_list]
    return category_urls


def get_book_urls(soup: BeautifulSoup) -> List[str]:
    book_library = soup.find_all("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    book_urls = [book.find("a")["href"] for book in book_library]
    return book_urls


def _get_rating(soup: BeautifulSoup) -> int:
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
    title = soup.find('h1').get_text()
    return title


def _get_category(soup: BeautifulSoup):
    book_breadcrumb = soup.find(class_='breadcrumb')
    category = book_breadcrumb.select('a')[2].get_text()
    return category


def _get_table_value(soup: BeautifulSoup, header_name: str):
    table = soup.find(class_="table")
    table_elements = table.find_all('tr')
    for element in table_elements:
        header = element.find('th')
        cells = element.find('td')
        if (header.contents[0]) == header_name:
            header_name = cells.contents[0]
            return header_name


def _get_description(soup: BeautifulSoup):
    book_para = soup.find(class_="product_page")
    description = book_para.find('p', recursive=False).get_text()
    return description


def _get_img(soup: BeautifulSoup):
    for item in soup.find_all('img'):
        image = (item['src'])
        return image


def scrap_book_url(url: str) -> Dict[str, Any]:
    pass


book_title = _get_title(book_soup)
book_category = _get_category(book_soup)
book_description = _get_description(book_soup)
book_image = _get_img(book_soup)
upc = _get_table_value(book_soup, 'UPC')
price_excl_tva = _get_table_value(book_soup, 'Price (excl. tax)')
price_incl_tva = _get_table_value(book_soup, 'Price (incl. tax)')
stock = _get_table_value(book_soup, 'Availability')
rating = _get_rating(book_soup)
print(book_description, book_category, book_image, upc, price_incl_tva, price_excl_tva, stock, rating)
library = get_book_urls(library_soup)
categories = get_category_urls(library_soup)
print(library)
print(categories)
category_url = _get_data('http://books.toscrape.com/' + library[0])
print(category_url)

""""
urls_list = [get_data('http://books.toscrape.com/' + library_url) for library_url in library]
souped_url = BeautifulSoup(urls_list, 'html.parser')
"""

"""
# Create an empty dictionary
book_features = {'category': book_category, 'description': book_description, 'image link': book_image, 'upc': upc,
                 'price excluding taxes': price_excl_tva, 'prince including taxes': price_incl_tva,
                 'in stock availability': stock, 'star rating': rating, 'title': book_title}
print(book_features)

book_features_csv = pd.DataFrame.from_dict(book_features, orient='index')
book_features_T_csv = book_features_csv.T
book_features_T_csv.to_csv("final_file.csv")
print(book_features_T_csv)
"""



