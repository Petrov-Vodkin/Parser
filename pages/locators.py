# coding=utf-8
class AvitoLocators:
    # HOST = "https://www.avito.ru/"
    URL_DDR4_SODIMM = 'https://www.avito.ru/omsk/tovary_dlya_kompyutera/komplektuyuschie/operativnaya_pamyat-' \
                      'ASgBAgICAkTGB~pm7gnYZw?cd=1&geoCoords=54.989342%2C73.368212&q=sodimm+ddr4&radius=50'
    URL_DDR4 = 'https://www.avito.ru/omsk/tovary_dlya_kompyutera/komplektuyuschie/operativnaya_pamyat-' \
               'ASgBAgICAkTGB~pm7gnYZw?cd=1&geoCoords=54.989342%2C73.368212&q=ddr4&radius=50'

    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"
    }

    ALL_PAGES = ".pagination-root-2oCjZ .pagination-item-1WyVp"
    ALL_PRODUCTS = ".iva-item-content-m2FiN .iva-item-body-NPl6W"

    PRODUCT_NAME = {"product_name": ['a', "title"]}
    PRODUCT_LINK = {"product_link": ["a", "href"]}
    PRODUCT_PRICE = {"product_price": [".iva-item-body-NPl6W .price-price-32bra [itemprop='price']", "content"]}

    PARAMS = {
        # 'cd': '1',
        # 'geoCoords': "54.989342%2C73.368212",
        # 'radius': "50"
        'p': None
    }
