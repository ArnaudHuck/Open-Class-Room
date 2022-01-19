# P2_Arnaud_Huck
Projet n°2 Books to scrap - BS4



## initialisation du projet: 

Dans Iterm :
Naviguez vers le repertoire souhaitez avec les commandes cd et ls


1. Récupérer le projet depuis github
	$ git clone https://github.com/ArnaudHuck/Project-2-Books-to-scrap.git


2. activer un environnement virtuel 
	$ cd P2_Arnaud_Huck 
	$ py -m venv env 
	$ source env/bin/activate


3. installer les dépendances du projet 
	$ pip install -r requirements.txt


4. executer le programme :
Scraping one book:
	$ python -c "from main import export_dictionary_and_image; export_dictionary_and_image('https://books.toscrape.com/catalogue/frankenstein_20/index.html', 'Frankenstein')"

Scraping a category: 
	$ python -c "from main import export_category_dictionaries_and_images; export_category_dictionaries_and_images('https://books.toscrape.com/catalogue/category/books/			mystery_3/index.html', 'mystery.csv')"


Scraping all the books:
	$ python -c "from main import export_categories_dictionaries_and_images; export_categories_dictionaries_and_images()"
