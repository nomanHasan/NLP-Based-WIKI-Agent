from DBConnection import DBConnection
from pycorenlp import StanfordCoreNLP
from SemregexManager import SemregexManager


class QuestionSemregex:
    def __init__(self):
        self.question = ""
        self.dbc = DBConnection()
        self.db = self.dbc.getDB()
        self.nlp = StanfordCoreNLP('http://localhost:9000')
        self.sm = SemregexManager()

    def set_question(self,q):
        self.question = q

    def get_output_semregex(self):
        patterns = self.db.semregexrules.find()
        for p in patterns:
            matched = False
            A = B = C = ""
            output = self.nlp.semgrex(self.question, pattern=p["Pattern"], filter=False)
            for e in output["sentences"]:
                for k in e.keys():
                    d = e[k]
                    if type(d) is dict:
                        A= d[u'$A'][u'text']
                        B = d[u'$B'][u'text']
                        C = d[u'$C'][u'text']
                        matched = True
            if matched:
                print "Compound ", self.sm.getCompound(self.question, C)
                C = self.sm.getCompound(self.question, C) + " " + C
                ret = [A, B, C, p["Output"], p["Type"]]
                print "Output Pattern", ret
                return ret