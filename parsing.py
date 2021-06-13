# coding=utf-8
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool as ThreadPool
from itertools import chain
from pages.locators import AvitoLocators
from pages.avito_page import AvitoPage
from pages.start_page import rand_proxy_from_file, rand_user_agents_from_file, save_in_json_file, save_in_csv_file

# url = AvitoLocators.URL_DDR4
print("Insert avito url, push Enter")
url = input()
proxy = rand_proxy_from_file
ua = rand_user_agents_from_file


def get_pagination_avito_content(num_page):
    params = {'p': num_page}
    parser_for_pagination = AvitoPage(url=url, params=params, proxy=proxy("proxies.txt"), user_agent=ua('desktop_ua.txt'))
    html_page = parser_for_pagination.response().text.encode('utf-8')
    pagination_content = parser_for_pagination.get_content(html_page)
    return pagination_content


parser_avito = AvitoPage(url=url, params=AvitoLocators.PARAMS, proxy=proxy("proxies.txt"), user_agent=ua('desktop_ua.txt'))
html_page = parser_avito.response().text.encode('utf-8')
first_page_content = parser_avito.get_content(html_page)

try:
    last_page_num = parser_avito.last_page_pagination(html_page)
    num_pages = [i for i in range(2, (int(last_page_num) + 1))]

    pool = ThreadPool(max(1, int(cpu_count() / 2)))
    all_pagination_content = pool.map(func=get_pagination_avito_content, iterable=num_pages)

    all_content = list(chain(first_page_content, *all_pagination_content))
    save_in_json_file(all_content)
    save_in_csv_file(all_content)

except Exception as ex:
    print("Pagination = 1", ex)
