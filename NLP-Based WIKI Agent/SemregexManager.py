from pycorenlp import StanfordCoreNLP
import re

class SemregexManager:
    def __init__(self):
        self.nlp = StanfordCoreNLP('http://localhost:9000')

    def getCompound(self, text, target):
        if not text or not target:
            return ""
        target = re.sub('\/', "-", target, 0)
        output = self.nlp.semgrex(text, pattern="{word:/"+target+"/}=A >compound {pos:/N.*/}=B", filter=False)
        compound = {}
        # print output
        if not output['sentences']:
            return ""
        for e in output["sentences"]:
            comp = []
            A = ""
            for k in e.keys():
                d = e[k]
                if type(d) is dict:
                    A = d[u'$A'][u'text']
                    B = d[u'$B'][u'text']
                    comp.append(B)
            comp.reverse()
            compound = ' '.join(comp)
            if compound:
                return compound
            else:
                return ""

    def getAdj(self, text, target):
        if not text or not target:
            return ""
        target = re.sub('\/', "-", target, 0)
        output = self.nlp.semgrex(text, pattern="{word:/"+target+"/}=A >amod {pos:/J.*/}=B", filter=False)
        # print "ADJ", output
        for e in output["sentences"]:
            comp = []
            A = ""
            for k in e.keys():
                d = e[k]
                if type(d) is dict:
                    A = d[u'$A'][u'text']
                    B = d[u'$B'][u'text']
                    comp.append(B)
            comp.reverse()
            compound = ' '.join(comp)
            if compound:
                return compound
            else:
                return ""

    def stem(self, text):
        if not text:
            return ""
        output = self.nlp.annotate(str(text), properties={'annotators': 'lemma', 'outputFormat': 'json'})
        return output['sentences'][0]['tokens'][0]['lemma']
