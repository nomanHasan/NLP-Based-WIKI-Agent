from bs4 import BeautifulSoup
from urllib2 import urlopen
import re

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', unicode(element)):
        return False
    return True

def cleaner_html(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    title = soup.find("h1", id="firstHeading")
    div = soup.find("div", id="mw-content-text")
    visible_text = ""
    for elem in div.findAll("p"):
        l = [" "]
        l+= filter(visible, elem.findAll(text=True))
        l = u" ".join(l)
        visible_text += l.encode('ascii','ignore')
    return title.get_text(), visible_text

def getTitle(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("h1", id = "firstHeading")
    return ''.join(title.findAll(text=True))

class HTMLHandler:
    def __init__(self):
        self.url = ""
        self.content = ""
        self.title=""
    def setUrl(self, url):
        self.url = url
        ch = cleaner_html(self.url)
        self.content = str(ch[1])
        self.title = str(ch[0])
    def getContent(self):
        self.content = re.sub('\([^\(\)]*\)', "", self.content, 0)
        self.content = re.sub('\([^\(\)]*\)', "", self.content, 0)
        self.content = re.sub('\[[^\[\]]*\]', "", self.content, 0)
        return self.content
    def getTitle(self):
        return self.title
