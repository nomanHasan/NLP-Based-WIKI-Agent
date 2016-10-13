from urllib import urlopen
from bs4 import BeautifulSoup
#
# print "What do you want to know about? "
#
# query = raw_input(":")
#
# print "query ", query

class WikiHandler:

    def __init__(self):
        self.wiki_org = "https://en.wikipedia.org"
        self.wikiSearch = "https://en.wikipedia.org/w/index.php?search="

    def searchQuery(self, query):
        self.query = query
        spaceless_query = query.replace(" ","+")
        finalQuery = self.wikiSearch+spaceless_query
        html = urlopen(finalQuery).read()
        soup = BeautifulSoup(html, 'html.parser')

        getURL = urlopen(finalQuery).geturl()

        if getURL==finalQuery:
            elems = soup.select('div .mw-search-result-heading')
            if len(elems) > 1:
                c = 1
                for e in elems:
                    print c, e.get_text()
                    c = c + 1

                sel = raw_input("Which one did you meant ? ")
                c = 0
                hr = ""
                sel = int(sel)
                for e in elems:
                    a = e.find('a')
                    if c == sel - 1:
                        hr = a['href']
                    c = c + 1

                print self.wiki_org + hr
                return self.wiki_org + hr
        else:
            returned_article = getURL.replace("https://en.wikipedia.org/wiki/","")
            returned_name = returned_article.replace("_"," ")
            print "Returned Name ", returned_name
            return getURL


