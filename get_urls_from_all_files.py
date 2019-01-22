import os
from bs4 import BeautifulSoup as Soup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from bs4.element import Comment
import urllib.request
import html2text


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


all_files = os.listdir("./rcnt")





for file in all_files:
    handle_urls = open("./urls/"+file, "w")
    str = ""
    handle = open("./rcnt/" + file)
    # print(handle.read())
    html = Soup(handle.read(), 'html.parser')
    for a in html.find_all('a', href=True):
        val = URLValidator()
        try:
            val(a['href'])
            if "webcache" not in a['href']:
                str += a['href'] + "\n"
                handle_urls.write(a['href'] + "\n")
            #print(html2text.html2text(a['href']))
            #html = urllib.request.urlopen(a['href']).read()
            #print(text_from_html(html))
        except ValidationError:
            print(ValidationError)

    handle_urls.write(str)
