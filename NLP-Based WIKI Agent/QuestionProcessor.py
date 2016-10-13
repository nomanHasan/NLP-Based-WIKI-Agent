from Sentence import Sentence
from SentenceManager import SentenceManager
from WikiHandler import WikiHandler
from HTMLHandler import HTMLHandler
from SummaryExtractor import SummaryExtractor
from WHADVP import WHADVP
from nltk.stem.porter import PorterStemmer
from QuestionSemregex import QuestionSemregex

class QuestionProcessor:
    def __init__(self):
        self.context = []
        self.WKH = WikiHandler()
        self.HTMH = HTMLHandler()
        self.porter_stemmer = PorterStemmer()
        self.qs = QuestionSemregex()

    def processWP(self, content, title):
        self.sumEx = SummaryExtractor(content, title)
        return ' '.join(self.sumEx.summary)

    def setParseString(self, parseString):
        self.parseString  = parseString
        sm = SentenceManager(self.parseString)
        sent = sm.getFirstSent()
        s1 = sent.root_node.children[0]
        if s1.name !="SBARQ":
            print "Its not a SBARQ"
            return ""
        if s1.children[0].name=="WHNP":
            print "Its a WHNP"
            if s1.children[0].children[0]:
                s2 = s1.children[0].children[0]
                wh = (s2.name, s2.value)
            print wh
            if s1.children[1].children[0]:
                s3 = s1.children[1].children[0]
                vb = (s3.name,s3.value)
            if s1.children[1].children[1]:
                s4 = s1.children[1].children[1]
                np = (s4.name, s4.get_text())
            print vb
            print np
            url = self.WKH.searchQuery(s4.get_text())
            self.HTMH.setUrl(url)
            title = self.HTMH.getTitle()
            content = self.HTMH.getContent()
            self.sumEx = SummaryExtractor(content, title)
            print ' '.join(self.sumEx.summary)
        elif s1.children[0].name=="WHADVP":
            print "Its a WHADVP"
            self.qs.set_question()

            # if s1.children[0].children[0]:
            #     s2 = s1.children[0].children[0]
            #     wh = (s2.name, s2.value)
            # print wh
            # if s1.children[1].children[2]:
            #     s3 = s1.children[1].children[2]
            #     vb = (s3.children[0].name, s3.children[0].value)
            # if s1.children[1].children[1]:
            #     s4 = s1.children[1].children[1]
            #     np = (s4.name, s4.get_text())
            # print vb
            # print np
            # url = self.WKH.searchQuery(s4.get_text())
            # self.HTMH.setUrl(url)
            # title = self.HTMH.getTitle()
            # content = self.HTMH.getContent()
            # whadv = WHADVP()
            # whadv.setText(content)
            # print whadv.getTimeOfAction(self.porter_stemmer.stem(vb[1]))
