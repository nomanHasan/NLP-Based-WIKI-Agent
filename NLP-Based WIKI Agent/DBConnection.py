from pymongo import MongoClient


class DBConnection:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.bot

    def getDB(self):
        return self.db


from datetime import datetime

client = MongoClient()
db = client.bot

db.notes.create_index("Title", unique= True)

try:
    result = db.notes.insert_one(
        {
            "Title":"First Note",
            "Date":datetime.now(),
            "Content":" This is the first Note that is being written in PyCharm and saved from the IDE to MongoDB"
        }
    )
except Exception:
    print "Note By this Title Already Exists "
try:
    result = db.notes.insert_one(
        {
            "Title":"Second Note",
            "Date":datetime.now(),
            "Content":" This is the first Note that is being written in PyCharm and saved from the IDE to MongoDB"
        }
    )
except Exception:
    print  "Note By this Title Already Exists "


result = db.notes.find()

for en in result:
    print en
    print "Title : ", en["Title"]
    print "Date : ", en["Date"]
    print en["Content"]

print "Index Information "
print db.articles.index_information()

# result = db.notes.delete_many({"$or":[{"Title": "First Note"}, {"Title": "Second Note"}]})
