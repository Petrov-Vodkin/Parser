# coding=utf-8
import datetime
from os import getpid
import requests
import json
import csv

from bs4 import BeautifulSoup
from random import choice


class ParserV2:
    def __init__(self, url, params="", parser="lxml", user_agent=None, proxy=None):
        self.url = url
        self.params = params
        self.parser = parser
        self.user_agent = user_agent
        self.proxy = proxy
        self.session = requests.session()

    @staticmethod
    def download_page(page, file_name_page="index.html"):
        try:
            with open(file_name_page, "w", encoding="utf-8") as file:
                file.write(page)
        except Exception as ex:
            print(f'Page not downloaded, Exception: {ex}')

    def response(self):
        self.session.proxies.update(self.proxy)
        self.session.headers.update(self.user_agent)
        response = self.session.get(self.url, params=self.params)
        print(f'{getpid()} Proxy {self.proxy}, URL {response.url}')
        assert response.status_code == 200, f'Status code ={response.status_code},url = {self.url}'
        self.session.close()
        return response

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


def rand_proxy_from_file(proxies_file):
    try:
        with open(f'data/{proxies_file}', 'r') as file:
            strings_file = file.read().splitlines()
            proxy = choice(strings_file).split('://')
            proxy_dict = {proxy[0]: proxy[1]}
            return proxy_dict
    except Exception as ex:
        print(f"Fail to chose random proxy from {proxies_file}, Exception {ex}")
        return None


def rand_user_agents_from_file(user_agent_file):
    try:
        with open(f'data/{user_agent_file}', 'r') as file:
            strings_file = file.read().splitlines()
            u_a = choice(strings_file)
            return {'user-agent': u_a}
    except Exception as ex:
        print(f"Fail to chose random user agent from {user_agent_file}, Exception {ex}")
        return None


def save_in_csv_file(data, file_name='avito.csv', mode='w'):
    try:
        csv_columns = data[0].keys()
        with open(f'results/{file_name}', mode, newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, csv_columns)
            writer.writeheader()
            for dict_content in data:
                writer.writerow(dict_content)
    except Exception as ex:
        print(f"CSV file don`t saved, Exception {ex}")


def save_in_json_file(file_dict, mode='w', file_name='all_products_dict.json'):
    try:
        with open(f'results/{file_name}', mode) as file:
            json.dump(file_dict, file, indent=4, ensure_ascii=False)
    except Exception as ex:
        print(f"JSON file don`t saved, Exception {ex}")
