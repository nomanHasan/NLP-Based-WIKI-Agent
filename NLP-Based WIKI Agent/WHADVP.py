from pycorenlp import StanfordCoreNLP
import nltk

nlp = StanfordCoreNLP('http://localhost:9000')

class WHADVP:
    def __init__(self):
        self.text = ""


    def setText(self, text):
        self.text = text

    def getTimeOfAction(self, lemma):
        sents = nltk.sent_tokenize(self.text)
        dateTimeList = []

        for i in range(0, len(sents)-1, 10):
            txt = ' '.join(sents[i: i+10])
            output = nlp.semgrex(txt,
                                 pattern='{}=A << nsubj  ( {lemma:'+lemma+'; pos:/VB.*/}=B >> {ner:TIME}=C | >>{ner:DATE}=C )',
                                 filter=False,
                                 )


            for e in output["sentences"]:
                time = []
                sub = ""
                for k in e.keys():
                    d = e[k]
                    if type(d) is dict:
                        print k, d[u'$C'][u'text']
                        time.append(d[u'$C'][u'text'])
                        sub = d[u'$A'][u'text']
                if time:
                    dateTimeList.append([sub, ' '.join(time)])
        return dateTimeList

    def locationOfEntity(self, entity):
        output = nlp.semgrex(self.text,
                             pattern='{pos:/N.*/} = A <nsubj ( {lemma:located;pos:JJ}=B > ( {pos:/N.*/}=C > case {pos:IN}=D) )',
                             filter=False)
        locationList = []

        for e in output["sentences"]:
            location = []
            name = ""
            for k in e.keys():
                d = e[k]
                if type(d) is dict:
                    print k, d[u'$C'][u'text']
                    location.append(d[u'$C'][u'text'])
                    sub = d[u'$A'][u'text']
            if time:
                locationList.append([sub, ' '.join(location)])

        output = nlp.semgrex(self.text,
                             pattern='{pos:/[PN].*/} = A < nsubj ( {pos:/N.*/}=C >case {pos:IN})',
                             filter=False)
        for e in output["sentences"]:
            location = []
            name = ""
            for k in e.keys():
                d = e[k]
                if type(d) is dict:
                    print k, d[u'$C'][u'text']
                    location.append(d[u'$C'][u'text'])
                    sub = d[u'$A'][u'text']
            if time:
                locationList.append([sub, ' '.join(location)])

        return locationList