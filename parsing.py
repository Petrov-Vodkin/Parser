# coding=utf-8
from multiprocessing import cpu_count
from pages.locators import AvitoLocators
from pages.avito_page import AvitoPage
from pages.start_page import rand_proxy_from_file, rand_user_agents_from_file, write_json_file, write_csv_file
from multiprocessing.dummy import Pool as ThreadPool
import os


def get_pagination_avito_content(num_page):
    params = {'p': num_page}
    print(f'PARAMS {params},  ID PROC {os.getpid()}')
    parser_to_pagination = AvitoPage(url=url, params=params, proxy=proxy("proxies.txt"),
                                     user_agent=u_a('desktop_user_agent.txt'))
    html = parser_to_pagination.get_page_html()
    all_content = parser_to_pagination.get_content(html)

    write_json_file(all_content, mode='a')
    write_csv_file(all_content, mode='a')


url = AvitoLocators.URL_DDR4
proxy = rand_proxy_from_file
u_a = rand_user_agents_from_file

parser_avito = AvitoPage(url=url, params=AvitoLocators.PARAMS, proxy=proxy("proxies.txt"),
                         user_agent=u_a('desktop_user_agent.txt'))
html_page = parser_avito.get_page_html()
content = parser_avito.get_content(html_page)
write_json_file(content)
write_csv_file(content)

try:
    last_page_num = parser_avito.last_page_pagination(html_page)
    num_pages = [i for i in range(2, (int(last_page_num) + 1))]

    pool = ThreadPool(max(1, int(cpu_count() / 2)))
    all_pagination_content = pool.map(func=get_pagination_avito_content, iterable=num_pages)

except Exception as ex:
    print("Pagination = 1", ex)
