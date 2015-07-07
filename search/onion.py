import random
import requests
from time import sleep
from bs4 import BeautifulSoup

import tangelo
import json


user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36"
]


def get_random_user_agent():
    return user_agents[random.randint(0, len(user_agents) - 1)]

def parse_html(content):
    soup = BeautifulSoup(content)
    ul = soup.body.ul
    links = ul.find_all('a')
    output = []
    for link in links:
        text = link.text
        href = link.get('href').split('=')[1]
        if not 'tor2web' in href:
            output.append({'title': text, 'url':href,'source':'ahmia'})
    return output


def get_search_results(term):
    user_agent = get_random_user_agent()
    headers = {'User-Agent': user_agent}
    payload = {'q': term}
    url = 'https://ahmia.fi/search/'
    sleep(1.0 + random.randint(0, 500) / 100)
    response = requests.get(url, headers=headers, params=payload)
    output = parse_html(response.text)
    return output, user_agent
