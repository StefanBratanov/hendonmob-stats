import requests
from bs4 import BeautifulSoup
import re


def get_soup(url) -> BeautifulSoup:
    page = requests.get(url, verify=False)
    return BeautifulSoup(page.content, "html.parser")


def text2number(text):
    return int(re.sub(r'[^\d]', "", text))
