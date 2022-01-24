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
	$ python main.py book https://books.toscrape.com/catalogue/frankenstein_20/index.html 		Frankenstein.csv

Scraping a category: 
	$ python main.py category https://books.toscrape.com/catalogue/category/books/mystery_3/index.html mystery.csv


Scraping all the books:
	$ python main.py all 
