from HTMLParser import HTMLParser
import re

import tangelo

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result_tag = False
        self.results = []
        self.result_count = ""
        self.link_tag = False
        self.current_link = None

    def handle_starttag(self, tag, attrs):
        if tag == "a" and len(attrs) == 2:
            if attrs[0][0] == "href" and str(attrs[0][1]).startswith("http"):
                self.current_link = attrs[0][1]
                self.link_tag = True
        elif tag == "div":
            for att in attrs:
                if att[0] == "id" and att[1] == "resultStats":
                    self.result_tag = True
                    break

    def handle_data(self, data):
        if self.result_tag:
            result_array = re.findall(r'\b\d\b|[0-9][0-9,.]+', data)
            tangelo.log(data)
            if len(result_array) > 0:
                self.result_count = "".join(map(lambda x: "".join(x.split(",")), result_array))
                tangelo.log(self.result_count)
            self.result_tag = False
        elif self.link_tag:
            self.results.append(dict(url=self.current_link, title=data, source='google'))
            self.current_link = None
            self.link_tag = False

    def get_results(self):
        return self.results

    def get_result_count(self):
        return self.result_count
