#!/usr/bin/python3
import urllib.request
import locale
import codecs
import sys
import json
import re
import dblplib as lib
import bibtexparser
from datetime import datetime, timezone

def getLocation(paper):
    if paper["ENTRYTYPE"] == "article":
        loc = paper["journal"]
        if loc == "CoRR":
            loc = "ariXv"
        return loc + " ("+paper["year"]+")"
    else:
        loc = paper["ID"]
        loc = re.sub('^.*?/', '', loc)
        loc = re.sub('/.*$', '',  loc).upper()
        if loc == "IWPEC":
            loc = "IPEC"
        if loc == "BIRTHDAY":
            return  paper["booktitle"] # + " ("+paper["year"]+")"
        return loc + " " + paper["year"]

def getMyTitleKey(title):
    title = title.strip().replace("\n"," ").lower()
    if title == 'the computational complexity of finding separators in temporal graphs':
        return "the complexity of finding small separators in temporal graphs"
    if title == 'facility location under matroid constraints: fixed-parameter algorithms and applications' or title == 'fixed-parameter algorithms for maximum-profit facility location under matroid constraints':
        return "representative families for matroid intersections, with applications to location, packing, and covering problems"
    if title == 'facility location under matroid constraints - fixed-parameter algorithms and applications':
        return "fixed-parameter algorithms for maximum-profit facility location under matroid constraints"
    if title == 'multistage s-t path: confronting similarity with dissimilarity in temporal graphs':
        return "multistage s-t path: confronting similarity with dissimilarity"
    if title == 'the computational complexity of finding temporal paths under waiting time constraints':
        return "finding temporal paths under waiting time constraints"
    return title    

def getTimestamp(text):
    #Thu, 18 Feb 2021 00:00:00 +0100
    return datetime.strptime(text, '%a, %d %b %Y %H:%M:%S %z')

page = urllib.request.urlopen('https://dblp.org/pid/194/2380.bib?param=1')
papers = dict()

def sortDatetime(val):
    #return getTimestamp(val['timestamp']).toordinal()
    return int(val['year'])


bib_database = bibtexparser.loads(page.read().decode("utf-8"))
bib_database.entries.sort(key=sortDatetime, reverse=True)

papers = dict()
for paper in bib_database.entries:
    title = getMyTitleKey(paper['title'])
    if title in papers:
        papers[title].append(paper)
    else:
        papers[title] = [paper]

def sortByYearCount(val):
    last = 0
    first = 2100
    #value = 0
    for pub in papers[val]:
        now = int(pub["year"])
        last = max(last,now)
        first = min(first,now)
        #value += now
    return last*100 + first*10

keys = list(papers.keys())
keys.sort(key = sortByYearCount, reverse = True)

for key in keys:
    paper = papers[key][0]
    print("<p>")
    authors = [s.replace("{\\'{e}}", "é").replace("{-}","-").strip() for s in paper["author"].split("and\n")]
    if len(authors) == 1:
        print(authors[0], end="")
    if len(authors) == 2:
        print(authors[0] + " and " + authors[1], end="")
    else:
        for name in authors:
            if authors[-1] == name:
                print("and "+name, end="")
            else:
                print(name+", ", end="")
    print(":<br>")
    print("<strong>" + paper['title'].replace("{","").replace("}","")+ "</strong><br>")
    for pub in papers[key]:
        print("<a href='" + pub["url"] + "'>")
        print(getLocation(pub))
        print("</a>")
        print("&nbsp;|&nbsp;")

    print("<a href='" + paper["biburl"] + "'>BibTeX</a>")
    print("</p>")

