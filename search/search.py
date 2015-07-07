import json

import tangelo

from htmlparser import MyHTMLParser
import google
import onion

def search_onion(term):
    quoted_term = '"%s"' % term
    (results, user_agent_onion) = onion.get_search_results(quoted_term)
    return results


def search_google(term):
    quoted_term = '"%s"' % term
    parser = MyHTMLParser()
    (html, user_agent_google) = google.get_search_results(quoted_term)
    parser.feed(html)
    # remove the last result which is the google location based search about
    # page
    del parser.get_results()[-1]
    return parser.get_results()

@tangelo.restful
def get(term):
    google_results = search_google(term)
    tangelo.log(google_results)
    onion_results = search_onion(term)
    tangelo.log(onion_results)
    results = google_results + onion_results
    if len(results) != 0:
        return json.dumps(dict(success=True, resultCount=len(results), results=results))
