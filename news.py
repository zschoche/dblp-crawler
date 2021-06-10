#!/usr/bin/python3
import urllib.request
import locale
import codecs
import sys
import json
import dblplib as lib
import bibtexparser
from datetime import datetime, timezone


def getTimestamp(text):
    #Thu, 18 Feb 2021 00:00:00 +0100
    return datetime.strptime(text, '%a, %d %b %Y %H:%M:%S %z')

page = urllib.request.urlopen('https://dblp.org/pid/194/2380.bib?param=1')
papers = dict()

def sortDatetime(val):
    #return getTimestamp(val['timestamp']).toordinal()
    return int(val['year'])

def getLocation(paper):
    if paper['ENTRYTYPE'] == "article":
        if paper['journal'] == "CoRR":
            return "on arXiv"
        else:
            return "in "+paper['journal']
    elif paper['ENTRYTYPE'] == "inproceedings":
        return "on the "+paper['booktitle'].split(',')[0].strip()

bib_database = bibtexparser.loads(page.read().decode("utf-8"))
bib_database.entries.sort(key=sortDatetime, reverse=True)

years= dict()
for paper in bib_database.entries:
    if paper['year'] not in years:
        years[paper['year']] = []
    years[paper['year']].append(paper)


for year in years.keys():
    print("<h1>{0}</h1>".format(year))
    years[year].sort(key=sortDatetime, reverse=True)
    for paper in years[year]:
        #print("<strong>{0}:</strong> ".format(getTimestamp(paper['timestamp']).strftime("%d %b %Y")),end="")
        print("Published ")
        print("<a href=\"{0}\">{1}</a>".format(paper['url'],paper['title'].replace("{","").replace("}","")))
        print(" "+getLocation(paper)+"<br>")
        authors = [s.replace("{\\'{e}}", "é").replace("{-}","-").strip() for s in paper["author"].split("and\n")]
        authors.remove('Philipp Zschoche')
        if len(authors) == 1:
            print("together with "+authors[0])
            print("<br>")
        if len(authors) > 1:
            print("together with",end=' ')
            for name in authors[:-1]:
                print(name,end=', ')
            print("and "+authors[-1])
            print("<br>")



def sortByYear(val):
    return int(papers[val][0]["year"])


