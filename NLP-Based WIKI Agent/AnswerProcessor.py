from pycorenlp import StanfordCoreNLP
from DBConnection import DBConnection
from nltk.stem.porter import PorterStemmer
import nltk
import re
from SemregexManager import SemregexManager


class AnswerProcessor:
    def __init__(self):
        self.answer = ""
        self.dbc = DBConnection()
        self.db = self.dbc.getDB()
        self.nlp = StanfordCoreNLP('http://localhost:9000')
        self.text = ""
        self.semregex = ""
        self.porter_stemmer = PorterStemmer()
        self.lemma = ""
        self.SM = SemregexManager()

    def set_text(self, text):
        self.text = text

    def set_lemma(self, le):
        le = self.SM.stem(le)
        self.lemma = le
        self.semregex= re.sub(r'LEMMA', le, self.semregex)
        print self.semregex

    def set_semregex(self, semr):
        self.semregex = semr
        print "semr ", self.semregex

    def execute_answer(self):
        if self.text == "" or self.semregex == "":
            return ""
        sents = nltk.sent_tokenize(self.text)

        ans_list = []

        for i in sents:
            output = self.nlp.semgrex(i, pattern=self.semregex, filter=False)

            for e in output["sentences"]:
                pred = []
                sub = ""
                verb = ""
                for k in e.keys():
                    d = e[k]
                    if type(d) is dict:
                        # print k, d[u'$C'][u'text']
                        C = d[u'$C'][u'text']
                        cmp = self.SM.getCompound(i, C)
                        adj = self.SM.getAdj(i, C)
                        C = adj + " " + cmp + " " + C
                        pred.append(C)
                        sub = d[u'$A'][u'text']
                        verb = d[u'$B'][u'text']
                pred = ' '.join(pred)
                if pred:
                    ans_list.append([sub, verb, pred])
        print ans_list
        return ans_list