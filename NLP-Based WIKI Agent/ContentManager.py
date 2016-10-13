from DBConnection import DBConnection
import nltk
from collections import Counter

class ContentManager:
    def __init__(self):
        self.dbc = DBConnection()
        self.db = self.dbc.getDB()

    def get_article(self, name):
        records = self.db.articles.find({"name": name})
        if records.count():
            for e in records:
                print e["aka"], type(e["aka"]), e["pronoun"], type([e["pronoun"]])
                return [[e["pronoun"]] + e["aka"]], e["content"]
        else:
            return ""

    def find_article(self, aka):
        result = self.db.articles.find(
            {
                "aka": {
                    "$in": [aka]
                }
            }
        )

        if not result.count():
            print "There was no Article by that Name ! "
            return 0
        else:
            for e in result:
                # self.set_pronoun(e["name"], highest_freq_pronoun(e["content"]))
                return [[e["pronoun"]] + e["aka"]], e["content"]

    def save_article(self, name, content):
        res = self.db.articles.find({"name": name})
        if res.count():
            return "Duplicate Article Exists !"
        else:
            print "No Duplicate, Saving Article "
        self.db.articles.insert_one(
            {
                "name": name,
                "content": content,
                "aka": [name],
                "pronoun": highest_freq_pronoun(content)
           }
        )
        print highest_freq_pronoun(content)
        return "Insertion Was Successful !"

    def update_article(self, name, content):
        self.db.articles.update_one(
            {"name": name},
            {
                "$set": {
                "content": content
                }
            }
        )
        return "Update Was Successful !"

    def add_aka(self, name, aka):
        self.db.articles.update_one(
            {"name": name},
            {
                "$push": {
                    "aka": aka
                }
            }
        )

    def set_pronoun(self, name, pronoun):
        self.db.articles.update_one(
            {"name": name},
            {
                "$set": {
                "pronoun": pronoun
                }
            }
        )
        return "Update Was Successful !"


def highest_freq_pronoun(text):
    wordList = []
    for word in nltk.word_tokenize(text):
        if len(word)>0 and "\\" not in word and nltk.pos_tag(nltk.word_tokenize(word))[0][1] == "PRP":
            wordList.append(word.lower())
    counts = Counter(wordList)
    print counts
    return counts.most_common(1)[0][0]