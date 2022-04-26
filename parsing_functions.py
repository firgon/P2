import re
import requests
from bs4 import BeautifulSoup

"""
:param indirect url
:return url without any "../"
"""


def clean_url(url):
    return url.replace("../", '')


"""
:param base_url, titre, category
:return dict with keys :
product_page_url
universal_product_code
title 
price_including_tax 
price_excluding_tax 
number_available 
category (as param)
product_description
review_rating
image_url
"""


def get_info_from_book(base_url, titre, category):
    result = dict()

    # build complete url
    result['product_page_url'] = base_url + "catalogue/" + titre

    # parse page
    page = requests.get(result['product_page_url'])
    soup = BeautifulSoup(page.content, "html.parser")

    result['category'] = category

    # title is inside h1
    result['title'] = soup.h1.text

    # product_description is in the next element after div id "product_description'
    subtitle = soup.find('div', id="product_description")
    if subtitle:
        description = subtitle.findNextSibling().text
        # delete ...More at the end
        result['product_description'] = str(description.removesuffix("...more"))
    else:
        result['product_description'] = ''

        # check each line of the table to seek if it is a needed data
    table = soup.findAll('tr')
    for line in table:
        if line.th.string == "UPC":
            result['universal_product_code'] = line.td.text

        elif line.th.string == "Price (excl. tax)":
            result['price_excluding_tax'] = line.td.text

        elif line.th.string == "Price (incl. tax)":
            result['price_including_tax'] = line.td.text

        elif line.th.string == "Availability":
            # keep only digit for availability
            result['number_available'] = re.sub('\\D', '', line.td.string)

    # rating is literal in 2nd class argument of star-rating container
    rating_container = soup.find('p', "star-rating")
    string_rating = rating_container['class'][1]
    # then we change it in digit
    possible_rating_values = ("Zero", "One", "Two", "Three", "Four", "Five")
    result['review_rating'] = possible_rating_values.index(string_rating)

    # image source is the first one on the page
    image_src = soup.find('img')['src']
    # to get the whole image url, we clean it and add base_url prefix
    result['image_url'] = base_url + clean_url(image_src)

    return result


"""search for any pages of a category given in parameter and collect all listed books

:param base_url, category_url
:return table with all indirect cleaned book urls
"""


def get_book_urls_from_category(base_url, category_url):
    result = []

    for x in range(1, 100):
        # load page (with index.html for the 1st page, or pageX.html for next)
        if x == 1:
            page = requests.get(base_url + category_url)
            # une fois la page 1 passée, il faut supprimer /index.html à la fin
            # pour préparer les pages suivantes
            category_url = category_url.removesuffix("/index.html")
        else:
            page = requests.get(base_url + category_url + '/page-' + str(x) + '.html')

        # if there is no corresponding webpage, return all already collected results
        if not page.ok:
            return result
        # otherwise parse the webpage
        else:
            soup = BeautifulSoup(page.content, "html.parser")

            # books url are in <a> in all <h3>
            for book in soup.findAll('h3'):
                href = book.a.get('href')
                titre = clean_url(href)
                result.append(titre)


""" function to get all category url from a website given in parameter 
return : a dict with category names in key and category indirect urls in objects
"""


def get_categories_from_website(base_url):
    # récupérer la page et la parser
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, "html.parser")

    result = dict()

    # get all <a> pointing on a category
    links = soup.findAll(href=re.compile("catalogue/category/books/"))

    for link in links:
        # clean category strings
        category = str(link.string).strip()
        result[category] = clean_url(link['href'])

    return result
