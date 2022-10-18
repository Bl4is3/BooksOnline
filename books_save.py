import requests
import csv
from bs4 import BeautifulSoup


def get_datas_for_one_product(product):
    product_page_url = url + "catalogue/" + product
    print(product_page_url)
    page = requests.get(product_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = []
    tables = soup.select('table > tr')
    for table in tables:
        elements.append(table.td.string.replace('<td>', ''))

    upc = elements[0]
    print("UPC :", upc)
    title = soup.find("div", class_="product_main").h1.string
    print("Titre :", title)
    price_excluding_tax = elements[2]
    print("Price.HT :", price_excluding_tax)
    price_including_tax = elements[3]
    print("Price.TTC :", price_including_tax)
    number_available = elements[5].replace('In stock (', '').replace('available)', '')
    print("Available : ", number_available)
    para = soup.find(id="product_description")
    if para:
        product_description = str(para.find_next_siblings('p')).replace('[<p>', '').replace('</p>]', '')
    else:
        product_description = ''
    print("Description :", product_description)
    image_url = soup.img['src']
    print("lien_image :", image_url)
    review_rating = elements[6]
    print("Reviews :", review_rating)
    liens = soup.select('ul.breadcrumb > li > a')
    category = liens[2].string
    print("Category :", category)

    en_tete = ["product_page_url", "universal_product_code", "title", "price_including_tax",
               "price_excluding_tax", "number_available", "product_description", "category",
               "review_rating", "image_url"]
    file = category + ".csv"
    with open(file, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(en_tete)
        writer.writerow([product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available,
                         product_description, category, review_rating, image_url])


def get_all_products_for_one_category(category):
    url_category = url + "catalogue/category/books/" + category
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


def get_all_categories(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    cats = soup.select("ul.nav-list > li > ul > li")
    categories = []
    for category in cats:
        cat = str(category.a["href"].replace('catalogue/category/books/', '').replace("/index.html", ""))
        categories.append(cat)
    return categories


url = "http://books.toscrape.com/"


def get_all_datas(url):
    categories = get_all_categories(url)
    for category in categories:
        products = get_all_products_for_one_category(category)
        for product in products:
            get_datas_for_one_product(product)


get_all_datas(url)
# categories = get_all_categories(url)
# for category in categories:
#     get_all_products_for_one_category(category)
#     products = get_all_products_for_one_category(category)
#     print(category)
#     for product in products:
#         print(product)
