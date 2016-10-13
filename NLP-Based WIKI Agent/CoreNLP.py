from pycorenlp import StanfordCoreNLP
import pprint
import nltk
from Sentence import Sentence

nlp = StanfordCoreNLP('http://localhost:9000')
text = (
    'Purgrug Vobter and Juklog Qligjar vruled into the Battlefield. Vobter was about to Hellfire. Juklog Qligjar started kiblaring.')
text = "When did Isaac Newton die ?"
output = nlp.annotate(text, properties={
    'annotators': 'tokenize,ssplit,pos,depparse,parse',
    'outputFormat': 'json'
})


print [s['parse'] for s in output['sentences']]

print [s['parse'].replace("\r"," ").replace("\n"," ").split(" ") for s in output['sentences']]

output = nlp.tokensregex(text, pattern='/Pusheen|Smitha/', filter=False)

output = nlp.semgrex(text, pattern='{tag: VBD}', filter=False)

output = nlp.annotate(text, properties={
    'annotators': 'tokenize,ssplit,pos,depparse,lemma,ner,parse,dcoref',
    'outputFormat': 'json'
})

ps = output['sentences'][0]['parse']

tokens = nltk.word_tokenize(ps)
print " ".join(tokens)

sent = Sentence(tokens)


sentence_root = sent.root_node

print len(sentence_root.children)
print "Printing Name of the Nodes "

sent.traverseDFS()

pp = pprint.PrettyPrinter(indent=4)

print "PRETTY PRINT"
pp.pprint(ps)
#
# out2 = output
#
# text2 = "He lived in Dhaka. He was a good man. He died in the morning. He died in 19th February, 1977."
# output = nlp.semgrex(text2, pattern='{}=A << nsubj  ( {lemma:die; pos:/VB.*/}=B >> {ner:TIME}=C | >>{ner:DATE}=C )', filter=False)
# pp.pprint(output)
#
# print "Length", len(output["sentences"][2]['0'])
# print output["sentences"][2]['0']
#
# dateTimeList = []
#
# for e in output["sentences"]:
#     time = []
#     name = ""
#     for k in e.keys():
#         d = e[k]
#         if type(d) is dict:
#             print k , d[u'$C'][u'text']
#             time.append(d[u'$C'][u'text'])
#             sub = d[u'$A'][u'text']
#     if time:
#         dateTimeList.append([sub, ' '.join(time)])
#
# print dateTimeList
# print time
#
#
# text = (
#     'Who is Isaac Newton ? Where is Bangladesh ? Where was he born ? When is christmas ?')
# out2 = nlp.annotate(text, properties={
#     'annotators': 'tokenize,ssplit,pos,depparse,parse',
#     'outputFormat': 'json'
# })
#
# print [w.keys() for w in output["sentences"]]
# for se in out2['sentences']:
#     sentpos = [t['pos'] for t in se['tokens']]
#     # print [t for t in se['tokens']]
#     sent = [t['word'] for t in se['tokens']]
#     sentpos = ' '.join(sentpos)
#     sent = ' '.join(sent)
#     print sentpos
#     print sent