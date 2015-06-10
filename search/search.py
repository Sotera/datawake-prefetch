import json

import tangelo

from htmlparser import MyHTMLParser
import google


@tangelo.restful
def get(term):
    quoted_term = '"%s"' % term
    parser = MyHTMLParser()
    (html, user_agent) = google.get_search_results(quoted_term)
    parser.feed(html)
    if len(parser.get_results()) != 0:
        # remove the last result which is the google location based search about
        # page
        del parser.get_results()[-1]
        return json.dumps(dict(success=True, resultCount=parser.get_result_count(), results=parser.get_results()))
    tangelo.log(user_agent)
    return json.dumps(dict(success=False, userAgent=user_agent))
