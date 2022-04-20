"""
script pour scraper tous les livres du site books.toscrape.com

"""
from parseur_util import *
from writer_util import *

# PROVISOIRE : on désigne manuellement une page du site internet
titre = "the-white-cat-and-the-monk-a-retelling-of-the-poem-pangur-ban_865"
base_url = "http://books.toscrape.com/"
category = None

infos_scrapees = scraper_une_page(base_url, titre, category)

# on crée un fichier csv prêt à recevoir les infos d'une première page
writer = Writer("Resultat_scraping.csv", infos_scrapees.keys())

# on enregistre cette première page
writer.enregistre_nouvelle_page(infos_scrapees)

writer.close()
