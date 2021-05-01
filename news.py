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
    return getTimestamp(val['timestamp']).toordinal()

def getLocation(paper):
    if paper['ENTRYTYPE'] == "article":
        if paper['journal'] == "CoRR":
            return "on arXiv"
        else:
            return "in "+paper['journal']
    elif paper['ENTRYTYPE'] == "inproceedings":
        return "in "+paper['booktitle'].split(',')[0].strip()


bib_database = bibtexparser.loads(page.read().decode("utf-8"))
print(bib_database.entries)
bib_database.entries.sort(key=sortDatetime, reverse=True)
for paper in bib_database.entries:
    print(getTimestamp(paper['timestamp']).strftime("%d %b %Y"))
    print(paper['title'])
    print("appeared "+getLocation(paper)+".")
    print(paper)
   #print("together with "+getLocation(paper)+".")

    print("------")


def sortByYear(val):
    return int(papers[val][0]["year"])


