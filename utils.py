import requests
from bs4 import BeautifulSoup
import re


def get_soup(url) -> BeautifulSoup:
    page = requests.get(url, verify=False)
    return BeautifulSoup(page.content, "html.parser")


def extract_id(url) -> int:
    match = re.search(r"n=\d+", url)
    if match:
        return text2number(match.group())
    else:
        return None

def normalise_whitespace(text) -> str:
    return ' '.join(text.split())

def text2number(text) -> int:
    return int(re.sub(r'[^\d]', "", text))
