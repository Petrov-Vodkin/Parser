# coding=utf-8
import os
import requests
import json
import csv

from bs4 import BeautifulSoup
from .locators import ProxyLocators
from random import choice


class ParserV2:
    def __init__(self, url, params="", parser="lxml", user_agent=None, proxy=None):
        self.url = url
        self.params = params
        self.parser = parser
        self.user_agent = user_agent
        self.proxy = proxy
        self.session = requests.session()

    def download_page(self, page, file_name_page="index.html"):
        try:
            with open(file_name_page, "w", encoding="utf-8") as file:
                file.write(page)
        except Exception as ex:
            print(f'Page not downloaded, Exception: {ex}')

    def get_page_html(self):
        start_page = self.session.get(self.url, headers=self.user_agent, proxies=self.proxy, params=self.params)
        print(f'{os.getpid()} Proxy {self.proxy}, URL {start_page.url}')
        assert start_page.status_code == 200, f'Status code ={start_page.status_code},url = {self.url}'
        html_start_page = start_page.text.encode('utf-8')
        start_page.close()
        return html_start_page

    def get_all_soup_objects_from_page(self, item_locator, html_page):
        try:
            soup = BeautifulSoup(html_page, self.parser)
            all_products_on_page = soup.select(item_locator)
            return all_products_on_page
        except Exception as ex:
            print(f'Fail to find soup {item_locator} on html page,  Exception: {ex}')

    def get_content_from_soup(self, soup_objects, **content_locators):
        content_of_all_objects = []
        for product in soup_objects:
            content_of_one_object = {}
            for name, selector in content_locators.items():
                content_of_one_object[str(name)] = product.select_one(selector[0])[selector[1]]
            content_of_all_objects.append(content_of_one_object)
        return content_of_all_objects

    def get_proxies(self):
        proxies = self.get_all_soup_objects_from_page(ProxyLocators.CONTENT_LIST)
        return proxies


def rand_proxy_from_file(proxies_file):
    try:
        with open(proxies_file, 'r') as file:
            strings_file = file.read().splitlines()
            proxy = choice(strings_file).split('://')
            proxy_dict = {proxy[0]: proxy[1]}
            return proxy_dict
    except Exception as ex:
        print(f"Fail to chose random proxy from {proxies_file}, Exception {ex}")
        return None


def rand_user_agents_from_file(user_agent_file):
    try:
        with open(user_agent_file, 'r') as file:
            strings_file = file.read().splitlines()
            u_a = choice(strings_file)
            return {'user-agent': u_a}
    except Exception as ex:
        print(f"Fail to chose random user agent from {user_agent_file}, Exception {ex}")
        return None


def write_csv_file(data, fie_name='avito.csv', mode='w'):
    try:
        csv_columns = data[0].keys()
        with open(fie_name, mode, newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, csv_columns)
            writer.writeheader()
            for dict_content in data:
                writer.writerow(dict_content)
    except Exception as ex:
        print(f"CSV file don`t write, Exception {ex}")


def write_json_file(file_dict, mode='w', file_name='all_products_dict.json'):
    try:
        with open(file_name, mode) as file:
            json.dump(file_dict, file, indent=4, ensure_ascii=False)
    except Exception as ex:
        print(f"JSON file don`t write, Exception {ex}")
