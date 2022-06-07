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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from webdriver_manager.firefox import GeckoDriverManager

from fake_useragent import UserAgent

from selenium.webdriver import ActionChains
from test import RequestHandler


class ProductGetter:
    def __init__(self, barcode):
        self.barcode = barcode

    def get_product_info_from_barcode(self):
        pass


class BarcodeFinderSite:
    def __init__(self, url):
        self.url = url

    def get_url(self, barcode):
        return f'{self.url}{barcode}'


def get_products_info_barcode_list(url):
    barcodes = get_barcodes()
    current_barcode = 0
    current_name = ''
    with open('result.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t')
        with open('number_of_parsed_barcodes.csv', 'r') as f:
            number_of_parsed_barcodes = int(f.read())
        for i in range(number_of_parsed_barcodes, len(barcodes)):
            barcode = barcodes[i]
            if barcode == current_barcode and current_name:
                # csvwriter.writerow([barcode, name])
                # print(f'barcode {barcode} done')
                continue
            else:
                current_barcode = barcode
                bar_url = url + barcode
                name = get_product_info_from_url_barcode_list(bar_url)
                current_name = name
                if not name:
                    write_number_of_parsed_barcodes(i)
                    print(f'{i} barcodes parsed')
                    return
                csvwriter.writerow([barcode, name])
                print(f'barcode {barcode} done')
                time.sleep(0.1)


def get_products_info_ean13():
    url = 'https://ean13.info/product.php?search='
    barcodes = get_barcodes()
    current_barcode = 0
    current_name = ''
    with open('result.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t')
        number_of_parsed_barcodes = get_number_of_parsed_barcodes()

        for i in range(number_of_parsed_barcodes, len(barcodes)):
            barcode = barcodes[i]
            if barcode == current_barcode and current_name:
                continue
            else:
                bar_url = url + barcode
                name = get_product_info_from_url_ean13(bar_url)

                current_barcode = barcode
                current_name = name

                if name:
                    print(name)
                    if name != 'Товар не найден в базе данных':
                        csvwriter.writerow([barcode, name])
                        print(f'barcode {barcode} done')
                        time.sleep(0.1)
                    else:
                        write_barcode_to_not_founded(barcode)
                else:
                    write_number_of_parsed_barcodes(i)
                    print(f'{i} barcodes parsed')
                    return


def write_barcode_to_not_founded(barcode):
    with open('not_founded_codes.txt', 'a') as f:
        fwriter = csv.writer(f)
        fwriter.writerow([barcode])


def get_number_of_parsed_barcodes():
    with open('number_of_parsed_barcodes.csv', 'r') as f:
        number_of_parsed_barcodes = int(f.read())
    return number_of_parsed_barcodes


def get_barcodes():
    with open('instances_fmcg_mining1.txt', 'r') as f:
        rows = f.readlines()
    barcodes = [row.split()[2] for row in rows]
    return barcodes


def write_number_of_parsed_barcodes(num):
    with open('number_of_parsed_barcodes.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([num])


def get_product_info_from_url_barcode_list(url):
    page_html = requests.get(url).text
    bs = BeautifulSoup(page_html, 'html.parser')
    barcode_table = bs.find('table', {'class': 'randomBarcodes'})
    # return barcode_table
    try:
        product_name = barcode_table.find_all('tr')[1].find_all('td')[2]
    except AttributeError:
        print(f'ERROR with url = {url}')
        return ''
    return product_name.get_text()


def get_product_info_from_url_ean13(url):
    page_html = requests.get(url).text
    bs = BeautifulSoup(page_html, 'html.parser')
    try:
        product_name = bs.find('div', {'class': 'item-card'}).find('div', {'class': 'col-lg-7'}).find('h1')
    except AttributeError:
        print(f'ERROR with url = {url}')
        return ''
    return product_name.get_text()


def set_selenium_driver(proxy: None):
    options = Options()
    ua = UserAgent(verify_ssl=False)
    userAgent = ua.random
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument("--disable-popup-blocking")
    # options.add_argument('headless')

    options = webdriver.FirefoxOptions()
    options.add_argument(f'user-agent={userAgent}')
    options.add_argument('headless')
    if proxy:
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument()
        options.add_argument(f'--proxy-server={proxy}')
    # binary = '/home/daniel/Downloads/firefox'

    gecko = "~/Downloads/geckodriver"
    firefox_binary = FirefoxBinary(gecko)
    # browser = webdriver.Firefox(firefox_binary=binary)
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    # driver = webdriver.Firefox(firefox_binary=firefox_binary, executable_path=gecko, options=options)
    return driver


def wait_between_calls():
    seconds = 120
    for i in range(seconds):
        time.sleep(1)
        if i % 10 == 0:
            print(f'{seconds - i} seconds left')


def get_products_by_barcode_progaonline():
    driver = set_selenium_driver()
    action = ActionChains(driver)
    driver.get('https://progaonline.com/kod')
    barcodes = get_barcodes()
    unique_barcodes = list(set(barcodes))
    text_to_send = ''
    for i in range(len(unique_barcodes) // 30):
        if i * 30 + 30 > len(unique_barcodes):
            barcodes_chunk = unique_barcodes[i*30:len(unique_barcodes)-1]
        else:
            barcodes_chunk = unique_barcodes[i*30:i*30+30]
        for barcode in barcodes_chunk:
            text_to_send += f'{barcode}\n'
    input_element = driver.find_element(By.ID, 'description')
    button = driver.find_element(By.CSS_SELECTOR, 'body > div > div:nth-child(2) > '
                                                  'form > div:nth-child(4) > input[type=submit]')
    action.move_to_element(input_element).click(input_element).send_keys(text_to_send).perform()
    action.move_to_element(button).click(button).perform()





if __name__ == '__main__':
    os.environ['GH_TOKEN'] = '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'
    while True:
        get_products_info_barcode_list('https://barcode-list.ru/barcode/RU/Поиск.htm?barcode=')
        get_products_info_ean13()
        wait_between_calls()
    # barcodes = get_barcodes()
    # with open('unique_barcodes_155-1000.csv', 'w+') as f:
    #     fwriter = csv.writer(f)
    #     current_bacrode = barcodes[155]
    #     for i in range(156, 1000):
    #         barcode = barcodes[i]
    #         if barcode != current_bacrode:
    #             fwriter.writerow([barcode])
    #             current_bacrode = barcode


    # rh = RequestHandler()
    # print(rh.working_proxies)
    # proxy = rh.get('https://www.upcdatabase.com/itemform.asp')
    # print(proxy)
    # driver = set_selenium_driver(proxy)
    # get_product_info_from_url_selenium('https://barcode-list.ru/barcode/RU/Поиск.htm?barcode=4602984020546', rh)
