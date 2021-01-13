from bs4 import BeautifulSoup
import urllib3
import requests
import sys

def PrettifyHTMLScrape(weburl):
    req = requests.get(weburl)
    htmlSource=req.content
    soup = BeautifulSoup(htmlSource,"html.parser")
    soup.prettify()
    #Text=soup.find("requisitionDescriptionInterface")
    #for text in Text.find_all_next():print(text)
    return soup.get_text()

souptext=PrettifyHTMLScrape("%s" %sys.argv[1])
print(souptext)
