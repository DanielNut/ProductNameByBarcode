import requests
from bs4 import BeautifulSoup


def get_product_info_from_url_ean13(url):
    page_html = requests.get(url).text
    bs = BeautifulSoup(page_html, 'html.parser')
    try:
        product_name = bs.find('div', {'class': 'item-card'})
        # result = product_name.find('div', {'class': 'col-lg-7'}).find('h1')
    except AttributeError:
        print(f'ERROR with url = {url}')
        return ''
    print(product_name)


if __name__ == '__main__':
    get_product_info_from_url_ean13('https://ean13.info/product.php?search=8682214703384')
