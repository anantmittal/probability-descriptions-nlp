import os
from bs4 import BeautifulSoup as Soup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from bs4.element import Comment
import urllib.request
import html2text
from pathlib import Path


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = Soup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


all_files = os.listdir("./urls")

for file in all_files:
    print(file)
    my_file = Path("./urls_data/" + file)
    if my_file.is_file():
        continue

    handle_url_data = open("./urls_data/" + file, "w")
    str = ""
    handle = open("./urls/" + file)
    urls_in_file = handle.readlines()
    for url in urls_in_file:
        print(url)
        try:
            html = urllib.request.urlopen(url).read()
            str += text_from_html(html)
        except Exception:
            print(Exception)
    handle_url_data.write(str)
    handle_url_data.close()
