import json
import os
import csv
import re
import time
import typing as tp
# import PIL
import concurrent.futures
import selenium.common.exceptions
import requests

from bs4 import BeautifulSoup

from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from webdriver_manager.firefox import GeckoDriverManager

from fake_useragent import UserAgent


import requests
from bs4 import BeautifulSoup
# from main import set_selenium_driver

# page_html = requests.get('https://barcode-list.ru/barcode/RU/Поиск.htm?barcode=4602984020546').text
# bs = BeautifulSoup(page_html, 'html.parser')
# barcode_table = bs.find('table', {'class': 'randomBarcodes'})
# print(barcode_table.find_all('tr')[1].find_all('td')[2].get_text())
os.environ['GH_TOKEN'] = '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'
# driver = set_selenium_driver()

#
# action = ActionChains(driver)


class RequestHandler:
    def __init__(self):
        print('Inititalizing working proxies...')
        self.proxy_list = []
        self.working_proxies = []
        with open('/Users/Drums/Documents/fmcg-scraper/proxies.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.proxy_list.append(row[0])
        self.get_working_proxies(self.proxy_list)

    def extract(self, proxy):
        url = 'https://www.upcdatabase.com/itemform.asp'
        try:
            resp = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=3)
            self.working_proxies.append(proxy)
        except:
            pass
        return proxy

    def get_working_proxies(self, proxies):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.extract, proxies)

    def get(self, url: str):
        """
        function for opening url through proxy
        :param url:
            url of web page
        :return:
            Html text
        """
        i = 0
        proxy = self.working_proxies[i]
        while i < len(self.working_proxies):
            try:
                proxies = {'http': proxy,
                           'https': proxy}
                response = requests.get(url, proxies=proxies, timeout=1)
                return proxy
            except:
                proxy = self.working_proxies[i]
                i += 1


def get_page_by_barcode_with_proxy_selenium(barcode):
    driver = set_selenium_driver()
    action = ActionChains(driver)
    get_product_info_by_barcode(barcode, driver, action)


def get_product_info_by_barcode(barcode, driver, action):
    driver.get('http://ru.disai.org/')

    input_element = driver.find_element(By.ID, 'search-form').find_element(By.TAG_NAME, 'input')
    button = driver.find_element(By.ID, 'search-form').find_element(By.TAG_NAME, 'a')
    action.move_to_element(input_element).click(input_element).send_keys(barcode).perform()
    action.move_to_element(button).click(button).perform()

    # table = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.caption > table:nth-child(1)')))
    font = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        '.caption > table:nth-child(1) > tbody:nth-child(1) >'
                                        ' tr:nth-child(2) > td:nth-child(1) > font:nth-child(1)')))
    print(font.text)


def set_selenium_driver():
    options = Options()
    ua = UserAgent(verify_ssl=False)
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--disable-popup-blocking")
    # options.add_argument('headless')

    options = webdriver.FirefoxOptions()
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument('headless')
    # binary = '/home/daniel/Downloads/firefox'

    gecko = "~/Downloads/geckodriver"
    firefox_binary = FirefoxBinary(gecko)
    # browser = webdriver.Firefox(firefox_binary=binary)
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    # driver = webdriver.Firefox(firefox_binary=firefox_binary, executable_path=gecko, options=options)
    return driver

# get_product_info_by_barcode('4602984020546', driver)
# get_product_info_by_barcode('4650067529462', driver)


if __name__ == '__main__':
    os.environ['GH_TOKEN'] = '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'
    # driver = set_selenium_driver()
    get_page_by_barcode_with_proxy_selenium('4607110521621')
