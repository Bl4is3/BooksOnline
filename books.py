import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import urllib.request
import shutil

URL_SITE = "http://books.toscrape.com/"


class BookToScrape:

    @classmethod
    def get_datas_for_one_product(cls, product, category):
        product_page_url = URL_SITE + "catalogue/" + product
        page = requests.get(product_page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        elements = []
        tables = soup.select('table > tr')
        for table in tables:
            elements.append(table.td.string.replace('<td>', ''))

        upc = elements[0]
        title = soup.find("div", class_="product_main").h1.string
        price_excluding_tax = elements[2]
        price_including_tax = elements[3]
        number_available = elements[5].replace('In stock (', '').replace('available)', '')
        para = soup.find(id="product_description")
        if para:
            product_description = str(para.find_next_siblings('p')).replace('[<p>', '').replace('</p>]', '')
        else:
            product_description = ''
        image_url = soup.img['src'].replace('../../', URL_SITE)
        product_name = soup.find("div", class_="product_main").h1.string
        name_img = "data/img/" + category + "/" + product_name.replace('/', '_') + ".jpg"
        urllib.request.urlretrieve(image_url, name_img)
        el = soup.select("div.product_main > p")
        if 'One' in str(el):
            review_rating = "1/5 stars"
        elif 'Two' in str(el):
            review_rating = "2/5 stars"
        elif 'Three' in str(el):
            review_rating = "3/5 stars"
        elif 'Four' in str(el):
            review_rating = "4/5 stars"
        elif 'Five' in str(el):
            review_rating = "5/5 stars"
        else:
            review_rating = ""
        file = "data/csv/" + category + ".csv"
        data_product = {
            "product_page_url": [product_page_url],
            "universal_product_code": [upc],
            "title": [title],
            "price_including_tax": [price_including_tax],
            "price_excluding_tax": [price_excluding_tax],
            "number_available": [number_available],
            "product_description": [product_description],
            "category": [category],
            "review_rating": [review_rating],
            "image_url": [image_url]
        }
        data_product_df = pd.DataFrame(data_product)
        data_product_df.to_csv(file, mode='a', index=False, header=False)

    @classmethod
    def get_all_products_for_one_category(cls, category):
        url_category = URL_SITE + "catalogue/category/books/" + category
        n = 1
        list_products = []
        while n != 0:
            if n == 1:
                suffix = "/index.html"
            else:
                suffix = "/page-" + str(n) + ".html"
            url_cat = url_category + suffix
            page = requests.get(url_cat)
            soup = BeautifulSoup(page.content, 'html.parser')
            all_products = soup.select("article > h3 ")
            for each_product in all_products:
                product = str(each_product.a["href"]).replace('../../../', '')
                list_products.append(product)
            pager = soup.select("ul.pager > li > a")
            if pager:
                n += 1
            else:
                n = 0
        return list_products

    @classmethod
    def get_all_categories(cls, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        cats = soup.select("ul.nav-list > li > ul > li")
        categories = []
        for category in cats:
            cat = str(category.a["href"].replace('catalogue/category/books/', '').replace("/index.html", ""))
            categories.append(cat)
            if not os.path.exists('data/img/' + cat):
                os.mkdir('data/img/' + cat)
            en_tete = {"product_page_url": [],
                       "universal_product_code": [],
                       "title": [],
                       "price_including_tax": [],
                       "price_excluding_tax": [],
                       "number_available": [],
                       "product_description": [],
                       "category": [],
                       "review_rating": [],
                       "image_url": []}
            file = "data/csv/" + cat + ".csv"
            en_tete_df = pd.DataFrame(en_tete)
            en_tete_df.to_csv(file, index=False, sep=",")
        return categories

    @classmethod
    def get_all_datas(cls, url):
        categories = BookToScrape.get_all_categories(url)
        for category in categories:
            products = BookToScrape.get_all_products_for_one_category(category)
            for product in products:
                BookToScrape.get_datas_for_one_product(product, category)

    def organisation(self):
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists('data/csv'):
            os.mkdir('data/csv')
        if not os.path.exists('data/img'):
            os.mkdir('data/img')

    def zip_datas(self):
        filename = "datas_zip"
        extension = "zip"
        directory = "data"
        if not os.path.exists(filename):
            shutil.make_archive(filename, extension, directory)


def main():
    bk = BookToScrape()
    bk.organisation()
    bk.get_all_datas(URL_SITE)
    bk.zip_datas()
