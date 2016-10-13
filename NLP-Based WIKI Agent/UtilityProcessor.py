import re
from datetime import datetime

class UtilityProcessor:
    def __init__(self):
        self.command = ""

    def giveCommand(self, cmd):
        self.command = cmd
        matchObj = re.match(r'^[Mm]ake a note by (.*)$', self.command, re.I)
        if matchObj:
            name = matchObj.group(1)
            print "Name", name
            inp = "Hello"
            cnt = ""
            while inp != "-finish-":
                inp = raw_input(":")
                cnt += inp
            note = Note(name)
            note.setContent(cnt)


class Note:
    def __init__(self,title):
        self.Title = title
        self.Content =""
        self.Date = datetime.now()

    def setContent(self,content):
        self.Content = content