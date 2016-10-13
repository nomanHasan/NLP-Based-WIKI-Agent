from collections import Counter
import nltk
import Chunker
import re

class SummaryExtractor:
    def __init__(self, text="",title="", ignoreList=["Jump"]):
        self.text = text
        self.title = title
        self.ignoreList = ignoreList
        self.nounCounter = self.NounCounter()
        self.getNickName()
        self.sentences = nltk.sent_tokenize(self.text)
        self.predicatesList = self.getPrediactesList()
        self.summary = self.getSummary()


    def HighestFreq(self):
        wordList = []
        for word in nltk.word_tokenize(self.text):
            if len(word)>3 and "\\" not in word and 'NN' in nltk.pos_tag(nltk.word_tokenize(word))[0][1] and word not in self.ignoreList:
                wordList.append(word)
        counts = Counter(wordList)
        return counts.most_common(1)[0][0]

    def NounCounter(self):
        wordList = []
        for word in nltk.word_tokenize(self.text):
            if len(word)>3 and "\\" not in word and 'NN' in nltk.pos_tag(nltk.word_tokenize(word))[0][1] and word not in self.ignoreList:
                wordList.append(word)
        counts = Counter(wordList)
        return counts

    def getNickName(self):
        self.nickName = self.nounCounter.most_common(1)[0][0]
        if self.nickName not in nltk.word_tokenize(self.title):
            self.nickName = nltk.word_tokenize(self.title)[1]
            print "Nickname ", self.nickName

    def getPrediactesList(self):
        predicatesList = []
        for sent in self.sentences:
            # print d, sent
            chunk = Chunker.ChunkSentence(sent, r"""
                                                NP: {<[CDJ,IPN].*>+}
                                                VERB: {<V.*>}
                                                BE: {<NP><VERB><NP>}
                                                """)
            for st in chunk.subtrees():
                if st.label()=='BE':
                    flag= False
                    scndNp=0
                    predicates = []
                    vMach = False
                    for s in st.subtrees():
                        if s.label()=="NP" and scndNp==0:
                            for w in s.leaves():
                               if re.search(".*"+self.nickName+".*",w[0],re.I):
                                   flag=True
                            scndNp=1
                        elif s.label()=='VERB' and flag:
                            if s.leaves()[0][0] in Chunker.be_verb_present+Chunker.be_verb_past:
                                vMach = True
                        elif s.label()=='NP' and scndNp>0 and flag and vMach:
                            scndNp=0
                            vMach=False
                            for el in s.leaves():
                                predicates.append(str(el[0]))
                            predicatesList.append(predicates)
        return predicatesList

    def getSummary(self):
        predicatesWeight=[]

        for pred in self.predicatesList:
            predWeight =0
            for word in pred:
                wordWeight = self.nounCounter[word]
                predWeight+=wordWeight
                # print word , wordWeight
            predicatesWeight.append(predWeight)
        ina = 100

        for i in range(0,len(predicatesWeight)):
            predicatesWeight[i] = (predicatesWeight[i]*ina)/(i+1)
            ina-=20

        return self.predicatesList[predicatesWeight.index(max(predicatesWeight))]

    def getPlace(self,target=""):
        if target=="":
            target = self.nickName
        for sent in self.sentences:
            chunk = Chunker.ChunkSentence(sent, r"""
                                                NP: {<[CDN].*>+}
                                                VERB: {<V.*>}
                                                PADJ: {<IN>}
                                                LOC: {<NP>.*<PADJ>.*<NP>}
                                                """)
            for st in chunk.subtrees():
                # print st
                if st.label()=="LOC":
                    print st
                    for s in st.subtrees():
                        if s.label()=="PADJ":
                            for l in s.leaves():
                                if l[0][0] in ["in","at"]:
                                    print st
