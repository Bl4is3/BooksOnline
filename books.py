import requests
import csv
from bs4 import BeautifulSoup


def datas_product(product_page_url):
    page = requests.get(product_page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = []
    tables = soup.table.find_all('tr')
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
    para = soup.find_all("p")
    product_description = para[3].string.replace('<p>', '').replace('</p>', '')
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
    file = name_category + ".csv"
    with open(file, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(en_tete)
        writer.writerow([product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available,
                         product_description, category, review_rating, image_url])


url = "http://books.toscrape.com/"
page_cat = requests.get(url)
soup1 = BeautifulSoup(page_cat.content, 'html.parser')
names_categories = []
categories = soup1.select("ul.nav-list > li > ul > li")
print(categories)
for cat in categories:
    name_category = str(cat.a["href"].replace('catalogue/category/books/', '').replace("/index.html", ""))
    url_category = url + "catalogue/category/books/" + name_category
    print("name", name_category)
    n = 1
    while n != 0:
        if n == 1:
            suffix = "/index.html"
        else:
            suffix = "/page-" + str(n) + ".html"
        url_cat = url_category + suffix
        print("URL cat", url_cat)
        page2 = requests.get(url_cat)
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        products = soup2.select("article > h3 ")
        for product in products:
            url_product = url + 'catalogue/'
            titre = str(product.a["href"]).replace('../../../', url_product)
            datas_product(titre)
            print("URL Product :", titre)
        pager = soup2.select("ul.pager > li > a")
        if pager:
            n += 1
        else:
            n = 0
