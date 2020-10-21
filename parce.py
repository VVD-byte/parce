import lxml
import requests
import logging
import re

logging.getLogger(__name__)

class parcer:
    def __init__(self):
        self.start_url = []

    def get(self, url):
        html = requests.get(url)
        return self.get_url(html.text)

    def get_url(self, text):
        return re.findall(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', text)

class data_base:
    def __init__(self):
        pass

#a = parcer()
#print(a.get())