import nltk


grammer2 = r"""
NP: {<C.*|IN|DT|JJ|NN.*>+}
PP: {<IN><NP>}
VP: {<VB.*><NP|PP|CLAUSE>+$}
CLAUSE: {<NP><VP>}
VERB: {<V.*>}
BE: {<NP>.*<V.*><NP>.*}
"""


be_verb_present = ['am', 'is', 'are', 'be']
be_verb_past = ['was', 'were']

def ChunkSentence(sentence, gram = grammer2, loop=1):
    sentence = nltk.pos_tag(nltk.word_tokenize(sentence))
    cp = nltk.RegexpParser(gram)
    if loop<2:
        result = cp.parse(sentence)
    else:
        result = cp.parse(sentence, loop)
    return result