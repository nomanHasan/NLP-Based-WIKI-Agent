import re
from pycorenlp import StanfordCoreNLP
from QuestionProcessor import QuestionProcessor
from UtilityProcessor import UtilityProcessor
from QuestionSemregex import QuestionSemregex
from AnswerProcessor import AnswerProcessor
from ContextManager import ContextManager

nlp = StanfordCoreNLP('http://localhost:9000')


print "Hello! I'm WikiBot As kme a Question or use Utility commands"

QP = QuestionProcessor()
UP = UtilityProcessor()
AP = AnswerProcessor()
CM = ContextManager()

inp = "Hello"

qs = QuestionSemregex()

def utility_command(cmd):
    UP.giveCommand(cmd)

while inp != "quit":
    inp = raw_input(":")
    match = re.match(r'^.*\?$', inp, re.I)
    if match:
        print "Its a question"
        # parseSent(inp)
        qs.set_question(inp)
        sem_value = qs.get_output_semregex()
        print sem_value
        CM.set_context(sem_value[2])
        content = CM.get_content()
        # print content
        print sem_value[4]
        subjList =[]
        for item in content[0][0]:
            l = item.split()
            subjList += l
        subjList = [s.lower() for s in subjList]
        print "Subject List ", subjList
        if sem_value[4] != "WP":
            print "Length : ", len(sem_value[3]), sem_value[3]
            AP.set_text(content[1])
            answers = []
            for sr in sem_value[3]:
                AP.set_semregex(sr)
                AP.set_lemma(sem_value[1])
                ansList = AP.execute_answer()
                print ansList
                answers += ansList
            print answers
            k = 0
            valid_answers = []
            for ans in answers:
                if ans[0].lower() in subjList:
                    valid_answers.append(answers[k])
                k += 1
            print "Valid Answers ", ' '.join(valid_answers[0])
        else:
            summary = QP.processWP(content[1], content[0][0][1])
            print sem_value[2] + " " + sem_value[1] + " " + summary
    else:
        print "It's a Utility Command"
        utility_command(inp)


def parseSent(inp):
    text = inp
    out = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse,parse',
        'outputFormat': 'json'
    })

    QP.setParseString(out['sentences'])

    for se in out['sentences']:
        pos = [t['pos'] for t in se['tokens']]
        # print [t for t in se['tokens']]
        sent = [t['word'] for t in se['tokens']]
        sentpos = list(zip(pos, sent))
        print "Sentpos ", sentpos
        pos = ' '.join(pos)
        sent = ' '.join(sent)
        print pos
        print sent



