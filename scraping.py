"""
script pour scraper tous les livres du site books.toscrape.com

"""
from parseur_util import *
from writer_util import *

base_url = "http://books.toscrape.com/"

infos_a_scraper = ('product_page_url',
                   'universal_product_code',
                   'title',
                   'price_including_tax',
                   'price_excluding_tax',
                   'number_available',
                   'category',
                   'product_description',
                   'review_rating',
                   'image_url')

categories = scraper_le_site(base_url)

for categorie in categories.keys():
    # on crée un fichier csv prêt à recevoir les infos demandées
    writer = Writer(categorie+".csv", infos_a_scraper)

    # on scrape la catégorie
    livres = scraper_une_category(base_url, categories[categorie])

    # pour chaque livre récupéré, on scrape la page correspondante
    for livre in livres:
        infos_scrapees = scraper_une_page(base_url, livre, categorie)

        # on enregistre cette première page
        writer.enregistre_nouvelle_page(infos_scrapees)

    # on ferme le fichier
    writer.close()
