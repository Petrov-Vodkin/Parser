# coding=utf-8
from pages.start_page import ParserV2
from pages.locators import AvitoLocators


class AvitoPage(ParserV2):
    def get_content(self, html_page):
        products = self.get_all_soup_objects_from_page(AvitoLocators.ALL_PRODUCTS, html_page)
        content = self.get_content_from_soup(products, **AvitoLocators.PRODUCT_NAME, **AvitoLocators.PRODUCT_PRICE,
                                               **AvitoLocators.PRODUCT_LINK)
        return content

    def last_page_pagination(self, html_page):
        pagination = self.get_all_soup_objects_from_page(AvitoLocators.ALL_PAGES, html_page)
        last_page = int(pagination[-2].text)
        print("Pagination = ", last_page)
        return last_page
