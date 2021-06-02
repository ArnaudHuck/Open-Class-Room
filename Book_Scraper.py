import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

URL = requests.get('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')
soup = BeautifulSoup(URL.content, 'html.parser')
# Finds all images
book_images = soup.find_all('img', {'src': re.compile('jpg')})
for book_image in book_images:
    print(book_image['src']+'\n')
Book_Data = soup.find(class_='container-fluid page')
Product_Information = Book_Data.find_all('tr')
# prints first Item found in Items
# print(Product_Information[0])
# print(Product_Information[0].find('th').get_text())
# print(Product_Information[0].find('td').get_text())

# Create an empty dictionary
book_dictionary = {}

# Finds all 'th' occurrences as a list
Product_Information_Name = [item.find('th').get_text() for item in Product_Information]
print(Product_Information_Name)
# Finds all 'td' occurrences as a list
Product_Information_Value = [item.find('td').get_text() for item in Product_Information]
print(Product_Information_Value)
# Finds first 'p' occurrence in the product_page direct children
product_page = soup.find(class_='product_page')
book_description = product_page.find('p', recursive=False).get_text()
# Finds book's title
books_title = soup.find(class_='col-sm-6 product_main')
book_title = books_title.find('h1').get_text()
book_ratings = books_title.find(class_='star-rating Three')
book_rating = book_ratings.find_all('i')
print(book_rating)
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
Product_Information_Name.append('Image Link')
book_dictionary['Image '] = book_image
Books_Features = pd.DataFrame([book_dictionary])

print(Books_Features)
Books_Features.to_csv('Book_Information.csv')
