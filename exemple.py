from books import BookToScrape, URL_SITE

category = "mystery_3"
bk = BookToScrape()
bk.organisation()
bk.get_all_categories(URL_SITE)
products = bk.get_all_products_for_one_category(category)
for product in products:
    bk.get_datas_for_one_product(product, category)
bk.zip_datas()
