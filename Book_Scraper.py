import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv


def get_data(url):
    r = requests.get(url)
    return r.text


URL = get_data('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')
soup = BeautifulSoup(URL, 'html.parser')
# Finds all images
for item in soup.find_all('img'):
    book_image = (item['src'])

Book_Data = soup.find(class_='container-fluid page')
Product_Information = Book_Data.find_all('tr')
# prints first Item found in Items
# print(Product_Information[0])
# print(Product_Information[0].find('th').get_text())
# print(Product_Information[0].find('td').get_text())

# Create an empty dictionary
book_dictionary = {}
# Finds all 'th' occurrences and set those as a list
Product_Information_Name = [item.find('th').get_text() for item in Product_Information]
Product_Information_Name.pop(1)
Product_Information_Name.pop(3)
Product_Information_Name.pop(4)
print(Product_Information_Name)
# Finds all 'td' occurrences and set those as a list
Product_Information_Value = [item.find('td').get_text() for item in Product_Information]
Product_Information_Value.pop(1)
Product_Information_Value.pop(3)
Product_Information_Value.pop(4)
print(Product_Information_Value)
# Finds 'p' occurrences then find in the product_page the first children
product_page = soup.find(class_='product_page')
book_description = product_page.find('p', recursive=False).get_text()
# Finds book's title
books_title = soup.find(class_='col-sm-6 product_main')
book_title = books_title.find('h1').get_text()
book_ratings = books_title.select('div > p')[1].get_text(strip=True)
print(book_ratings)
book_rating = ('1 star', '2 stars', '3 stars', '4 stars', '5 stars')

'''
if 'One' in book_ratings:
    book_rating = book_rating[0]
    print(book_rating)
if 'Two' in book_ratings:
    book_rating = book_rating[1]
    print(book_rating)
if 'Three' in book_ratings:
    book_rating = book_rating[2]
    print(book_rating)
if 'Four' in book_ratings:
    book_rating = book_rating[3]
    print(book_rating)
if 'Five' in book_ratings:
    book_rating = book_rating[4]
    print(book_rating)
'''

# Finds book's category
book_profile = soup.find(class_='breadcrumb')
book_categories = book_profile.find_all('li')
book_category = book_categories[2].get_text()

for num, name in enumerate(Product_Information_Name, start=0):
    print(f'Product_Information {num}: {name}, value: {Product_Information_Value[num]}')
    book_dictionary[name] = Product_Information_Value[num]

Product_Information_Name.append('Description')
book_dictionary['Description'] = book_description
Product_Information_Name.append('Title')
book_dictionary['Title'] = book_title
Product_Information_Name.append('Category')
book_dictionary['Category'] = book_category
Product_Information_Name.append('Rating')
book_dictionary['Rating'] = book_rating
Product_Information_Name.append('Image_Link')
book_dictionary['Image_Link'] = ()

Books_Features = pd.DataFrame([book_dictionary])

print(Books_Features)
Books_Features.to_csv('Book_Information.csv')
