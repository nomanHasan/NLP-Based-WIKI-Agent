from chatterbot import ChatBot

chatbot = ChatBot(
    'Study Assistant',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)


# Training
chatbot.train("chatterbot.corpus.english")

inp = "Hello"

while inp != "quit":
    inp = raw_input(":")
    print chatbot.get_response(inp)
