from typing import List, Dict
import csv
from scrap_category_url import scrap_category_books
from scrap_category_url import scrap_home_books
from scrap_category_url import get_category_urls
from scrap_category_url import scrap_all_categories
from scrap_page_url import join_category_url
from scrap_page_url import scrap_page_books_category
from Book_Scraper import scrap_book_url


def export_to_csv(dict_list: List[Dict], file_name: str):
    keys = dict_list[0].keys()
    with open(file_name, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)


# export_to_csv(scrap_home_books('https://books.toscrape.com/catalogue/page-1.html'), 'home.csv')
# export_to_csv(scrap_category_books('https://books.toscrape.com/catalogue/category/books/mystery_3/index.html')
#              , 'mystery.csv')
# print(get_category_urls('https://books.toscrape.com/index.html'))
# print(scrap_all_categories('https://books.toscrape.com/index.html'))
# print(join_category_url('catalogue/category/books/travel_2/index.html'))
print(scrap_book_url('https://books.toscrape.com/catalogue/the-past-never-ends_942/index.html'))