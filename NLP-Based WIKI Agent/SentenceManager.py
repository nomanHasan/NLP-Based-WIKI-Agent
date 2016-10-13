import nltk
from Sentence import Sentence


class SentenceManager:
    def __init__(self, parseStrings):
        self.parseStrings = parseStrings
        self.sentences = []

        for s in parseStrings:
            ps = s['parse']
            tokens = nltk.word_tokenize(ps)
            print " ".join(tokens)
            sent = Sentence(tokens)
            self.sentences.append(sent)

    def getFirstSent(self):
        return self.sentences[0]