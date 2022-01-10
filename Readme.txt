Project 2 : Books to scrap

SET YOU WORK ENVIRONMENT 

1. Open the following GitHub link: https://github.com/ArnaudHuck/Project-2-Books-to-scrap
2. Click on CODE and copy the following SSH link :
git@github.com:ArnaudHuck/Project-2-Books-to-scrap.git
3. Open your terminal and use the git clone command followed by the clone link
4. Open the Project-2-Books-to-scrap folder
5. Open your IDE and your folder
6. Create your virtual environment using : python -m venv env in your terminal
7. Activate your virtual environment using : source env/bin/activate
8. Install all required methods libraries using :
pip install -r requirements.txt


Open the https://books.toscrape.com/index.html url


Scraping one book:
1. Choose a book you want to scrap and get its url
2. Use the scrap_book_url function on the book's url:

UsedURL : Https://Books.Toscrape.Com/Catalogue/Frankenstein_20/Index.Html
Command : export_single_book_to_csv(scrap_book_url('https://books.toscrape.com/catalogue/	  frankenstein_20/index.html'), 'Frankenstein.csv')


Scraping a category:
1. Choose a category page you want to scrap and get its url
2. Use the scrap_category_books function on the page url

UsedURL : https://books.toscrape.com/catalogue/category/books/mystery_3/index.html
Command : export_list_to_csv(scrap_category_books('https://books.toscrape.com/catalogue/	  category/books/mystery_3/index.html'), 'mystery.csv')


Scraping all the books:
1. use the following url https://books.toscrape.com/catalogue/page-1.html
2. Use the scrap_home_books on the given url

UsedURL : https://books.toscrape.com/catalogue/page-1.html
Command : export_list_to_csv(scrap_home_books('https://books.toscrape.com/catalogue/		  page-1.html'), 'home.csv')

