import os
import logging

import pdfkit  # pip install pdfkit
import requests  # pip install requests
from lxml.etree import HTML  # pip install lxml

logging.basicConfig(
    level=logging.INFO,
    filename='html2pdf.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

airflow_version = '2.0.1'

home_page = f'https://airflow.apache.org/docs/apache-airflow/{airflow_version}/'

# get document urls
urls = []
logger.info('start to get airflow documents url')
resp = requests.get(home_page)
tree = HTML(resp.text)
for url_suffix in tree.xpath('//div[@class="toctree"]//a/@href'):
    url = home_page + url_suffix
    urls.append(url)

logger.info(f'total url num is: {len(urls)}, url list: {urls}')

tmp_dir = 'tmp'
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

# html to pdf
for index, url in enumerate(urls):
    try:
        pdfkit.from_url(url, f'{tmp_dir}/{index}.pdf')
        logger.info(f'page {index} download success, url is {url}')
    except:
        logger.error(f'page {index} download failed, url is {url}')
