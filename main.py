from books import BookToScrape, URL_SITE


bk = BookToScrape()
bk.organisation()
bk.get_all_datas(URL_SITE)
bk.zip_datas()

