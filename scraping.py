"""
script to scrap all books on books.toscrape.com website
"""

import parsing_functions
import os
import csv
import urllib.request
import re

base_url = "http://books.toscrape.com/"

needed_informations = ('product_page_url',
                       'universal_product_code',
                       'title',
                       'price_including_tax',
                       'price_excluding_tax',
                       'number_available',
                       'category',
                       'product_description',
                       'review_rating',
                       'image_url')

# create results folder
file_path = os.getcwd() + '\\Results\\'
img_file_path = file_path + 'img\\'

if not os.path.exists(file_path):
    os.mkdir(file_path)

if not os.path.exists(img_file_path):
    os.mkdir(img_file_path)

categories = parsing_functions.get_categories_from_website(base_url)
index = 0

for category in categories.keys():

    # open a csv file to store infos
    with open(file_path + category + '.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, needed_informations)
        writer.writeheader()

        # parse category
        books = parsing_functions.get_book_urls_from_category(base_url, categories[category])

        # for each books, parse infos
        for book in books:
            index = index + 1
            print(str(index) + " : " + book)

            needed_informations = parsing_functions.get_info_from_book(base_url, book, category)
            writer.writerow(needed_informations)

            # and download image in img folder
            # rename all image with book title + ID + extension

            # get extension first
            last_dot = needed_informations['image_url'].rindex('.')
            extension = needed_informations['image_url'][last_dot:]

            # get title then
            title = re.sub('\\W+', '-', needed_informations['title'])

            filename = title + extension

            # if a same file already exists add an index
            index = 2
            while os.path.exists(img_file_path + filename):
                filename = title + '(' + index + ')' + extension
                index += 1

            urllib.request.urlretrieve(needed_informations['image_url'],
                                       img_file_path + filename)
