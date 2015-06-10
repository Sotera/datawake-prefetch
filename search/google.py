import random
import urllib2
import urllib
from time import sleep

import tangelo


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


def get_search_results(term):
    user_agent = get_random_user_agent()
    params = dict()
    params["num"] = 50
    params["pws"] = 0
    params["gl"] = "US"
    params["q"] = term.encode("utf-8")
    url = "http://www.google.com/search?" + urllib.urlencode(params)
    tangelo.log(url)
    request = urllib2.Request(url)
    request.add_header("User-Agent", user_agent)
    sleep(1.0 + random.randint(0, 500) / 100)
    f = urllib2.urlopen(request)
    encoding = f.headers.getparam('charset')
    return f.read().decode(encoding), user_agent
