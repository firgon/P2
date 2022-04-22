import re
import requests
from bs4 import BeautifulSoup

"""
fonction qui reçoit en argument une url indirecte (commençant par ../) et la renvoie nettoyée
"""


def nettoyer_url(url):
    return url.replace("../", '')


"""
fonction qui reçoit l'adresse d'une page livre du site books.toscrape.com et parse son contenu :
product_page_url url
universal_product_code (upc) *
title <h1>
price_including_tax *
price_excluding_tax *
number_available *
category (envoyée en argument)
product_description <p> apres div product_description .next_sibling
review_rating p class star-rating
image_url img source
"""


def scraper_une_page(base_url, titre, category):
    resultat = dict()
    # construire l'adresse
    resultat['product_page_url'] = base_url + "catalogue/" + titre

    # récupérer la page et la parser
    page = requests.get(resultat['product_page_url'])
    soup = BeautifulSoup(page.content, "html.parser")

    resultat['category'] = category

    # le titre se trouve dans la balise h1
    resultat['title'] = soup.h1.string

    # la description se trouve après le sous-titre product_description
    soustitre = soup.find('div', id="product_description")
    description = soustitre.findNextSibling().string
    # on supprime ...More en fin de description
    resultat['product_description'] = description.removesuffix("...more")

    # on récupère toutes les infos du tableau et on les utilise en fonction de la valeur d'entête
    tableau = soup.findAll('tr')
    for ligne in tableau:
        if ligne.th.string == "UPC":
            resultat['universal_product_code'] = ligne.td.string

        elif ligne.th.string == "Price (excl. tax)":
            resultat['price_excluding_tax'] = ligne.td.string

        elif ligne.th.string == "Price (incl. tax)":
            resultat['price_including_tax'] = ligne.td.string

        elif ligne.th.string == "Availability":
            resultat['number_available'] = re.sub('\\D', '', ligne.td.string)

    # le rating (sous forme littérale) se trouve en 2e argument class du conteneur star-rating
    rating_conteneur = soup.find('p', "star-rating")
    string_rating = rating_conteneur['class'][1]
    # que l'on transforme en chiffre
    possibles_valeurs_rating = ("Zero", "One", "Two", "Three", "Four", "Five")
    resultat['review_rating'] = possibles_valeurs_rating.index(string_rating)

    # l'image source est la première
    image_src = soup.find('img')['src']
    # on lui enlève ../../ et l'on rajoute la base url du site
    resultat['image_url'] = base_url + nettoyer_url(image_src)

    return resultat


"""
fonction qui reçoit l'adresse d'une category du site books.toscrape.com
et renvoie une liste tous les titres dans cette category
"""


def scraper_une_category(base_url, category_url):
    resultat = []

    for x in range(1, 100):
        # charge la page (avec le suffixe index.html ou pageX.html suivant le cas)
        if x == 1:
            page = requests.get(base_url + category_url + "/index.html")
        else:
            page = requests.get(base_url + category_url + '/page-' + str(x) + '.html')

        # si le chargement a échoué, on renvoie les résultats déjà obtenus
        if page.status_code != 200:
            return resultat
        # sinon on parse la page
        else:
            soup = BeautifulSoup(page.content, "html.parser")

            # les url des livres sont dans des <a> dans de tous les <h3> de la page
            for book in soup.findAll('h3'):
                href = book.a.get('href')
                titre = nettoyer_url(href).removesuffix('/index.html')
                resultat.append(titre)


def scraper_le_site(base_url):
    # récupérer la page et la parser
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, "html.parser")

    resultat = dict()

    # extraire tous les liens pointant vers une categorie
    liens = soup.findAll(href=re.compile("catalogue/category/books/"))

    for lien in liens:
        # nettoyer l'affichage des categorie
        category = str(lien.string).strip()
        resultat[category] = lien['href']

    return resultat
