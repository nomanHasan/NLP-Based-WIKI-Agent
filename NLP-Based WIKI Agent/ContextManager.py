from ContentManager import ContentManager
from WikiHandler import WikiHandler
from HTMLHandler import HTMLHandler
import nltk
import re

class ContextManager:
    def __init__(self):
        self.context = []
        self.context.append("Isaac Newton")
        self.content = ""
        self.cm = ContentManager()
        self.WKH = WikiHandler()
        self.HTMH = HTMLHandler()

    def set_context(self, c):
        w = nltk.word_tokenize(c)
        first_pos = nltk.pos_tag(w)[0][1]
        print first_pos
        matchObj = re.match("N.*", first_pos, re.I)
        if matchObj:
            self.context.append(c)
        print "Context Name", self.get_context()

    def get_context(self):
        return self.context[len(self.context)-1]

    def get_content(self):
        aka = self.get_context()
        result = self.cm.find_article(aka)
        if result:
            return result
        else:
            url = self.WKH.searchQuery(aka)
            self.HTMH.setUrl(url)
            title = self.HTMH.getTitle()
            print "Title ", title
            self.set_context(title)
            res = self.cm.get_article(title)
            if res:
                self.cm.add_aka(title, aka)
                return res
            else:
                print "Saving Article to the Database"
                content = self.HTMH.getContent()
                self.cm.save_article(title, content)
                if title != aka:
                    self.cm.add_aka(title, aka)
                return self.cm.get_article(title)



