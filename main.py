import os
import logging

import pdfkit  # pip install pdfkit
import requests  # pip install requests
from lxml.etree import HTML  # pip install lxml


logger = logging.getLogger(__name__)

airflow_version = '2.0.1'

home_page = f'https://airflow.apache.org/docs/apache-airflow/{airflow_version}/'

# get document urls
urls = []
resp = requests.get(home_page)
tree = HTML(resp.text)
for url_suffix in tree.xpath('//div[@class="toctree"]//a/@href'):
    url = home_page + url_suffix
    urls.append(url)

tmp_dir = 'tmp'
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

# html to pdf
for index, url in enumerate(urls):
    try:
        pdfkit.from_url(url, f'{tmp_dir}/{index}.pdf')
        print('SUCCESS', index, url)
    except:
        print('ERROR', index, url)
