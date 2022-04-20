"""
fonction qui reçoit une adresse du site books.toscrape.com et parse son contenu :
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
import re
import requests
from bs4 import BeautifulSoup


def scraper_une_page(base_url, titre, category):
    resultat = dict()
    # construire l'adresse
    resultat['product_page_url'] = base_url + "catalogue/" + titre + "/index.html"

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
    possibles_valeurs_rating = ("Zero", "One", "Two", "Three", "Four")
    resultat['review_rating'] = possibles_valeurs_rating.index(string_rating)

    # l'image source est la première
    image_src = soup.find('img')['src']
    # on lui enlève ../../ et l'on rajoute la base url du site
    resultat['image_url'] = image_src.replace("../../", base_url)

    return resultat
