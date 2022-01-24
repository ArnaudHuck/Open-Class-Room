import csv
import os
import sys
from scrap_category_url import get_category_urls, next_page_url, scrap_category_books, export_list_to_csv, export_single_book_to_csv
from typing import Dict, List, Tuple, Any
from Book_Scraper import scrap_book_url
import os.path


base_url = 'https://books.toscrape.com/index.html'


def export_categories_dictionaries_and_images() -> List[Tuple[str, List[Dict]]]:
    """
    :param: Give 'https://books.toscrape.com/catalogue/page-1.html' url
    :return: Create a list of tuples with category name and dictionary. Exports the dictionary to csv using
    the category name as file name
    """
    category_urls_and_names = get_category_urls(base_url)
    all_category_and_dictionary_tuples = [
        (category_url_and_name[1] + '.csv', scrap_category_books(category_url_and_name[0])) for
        category_url_and_name in category_urls_and_names]
    os.getcwd()
    for category_and_dictionary_tuple in all_category_and_dictionary_tuples:
        export_list_to_csv(category_and_dictionary_tuple[1], (category_and_dictionary_tuple[0]))


def export_dictionary_and_image(url: str, file_name: str) -> Dict:
    export_single_book_to_csv(scrap_book_url(url), file_name)


def export_category_dictionaries_and_images(url: str, category_name: str) -> List[Dict]:
    export_list_to_csv(scrap_category_books(url), category_name)


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 3:
        if args[0] == 'category':
            export_category_dictionaries_and_images(args[1], args[2])
        elif args[0] == 'book':
            export_dictionary_and_image(args[1], args[2])
        else:
            print("Invalid parameters")
    elif len(args) == 1:
        if args[0] == 'all':
            export_categories_dictionaries_and_images()
    else:
        print("Invalid parameters")


# export_dictionary_and_image('https://books.toscrape.com/catalogue/spark-joy-an-illustrated-master-class-on-the-art-of-organizing-and-tidying-up_927/index.html',
#                            'Spark Joy An Illustrated Master Class on the Art of Organizing and Tidying Up.csv')
# export_category_dictionaries_and_images('https://books.toscrape.com/catalogue/category/books/mystery_3/index.html',mystery.csv 'm')
export_categories_dictionaries_and_images()
