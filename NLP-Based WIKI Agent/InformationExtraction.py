import nltk
from nltk.corpus import conll2000


def evalualteGrammer(grammer):
    cp = nltk.RegexpParser(grammer)
    test_sents = conll2000.chunked_sents('test.txt', chunk_types = ['NP'])
    print cp.evaluate(test_sents)

# evalualteGrammer(r"NP: {<[CDJNP].*>+}")


def pos_tag(sent):
    return nltk.pos_tag(nltk.word_tokenize(sent))

def parse_sentence(grammer,sent):
    cp = nltk.RegexpParser(grammer)
    print cp.parse(pos_tag(sent))


grammer = r""" NP: {<[CDJNP].*>+}"""
grammer2 = "NP: {<DT><JJ.*><NN.*>}"

evalualteGrammer(grammer)
evalualteGrammer(grammer2)


class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.UnigramTagger(train_data)

    def parse(self, sentence):
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag) in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)


test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
unigram_chunker = UnigramChunker(train_sents)
print(unigram_chunker.evaluate(test_sents))
