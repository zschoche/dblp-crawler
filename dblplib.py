import urllib.request
import locale
import codecs
import sys
import json

def printLocationDBLP(paper):
    last = ""
    if 'pages' in paper:
        last = ":"
    print(paper['venue'], end=" ")
    if 'volume' not in paper:
        print(paper['year'], end=last)
    else:
        print(paper['volume'], end=last)

    if 'pages' in paper:
        print(" " + paper['pages'], end="")
    if 'volume' in paper:
        print(" (" + paper['year'] + ")",end="")

def printLocationShort(paper):
    if paper['venue'] == 'CoRR':
        print("arXiv", end=" ")
    else:
        print(paper['venue'], end=" ")

    if 'volume' not in paper:
        print(paper['year'], end="")
    else:
        print("(" + paper['year'] + ")",end="")

def lookahead(iterable):
    """Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).
    """
    # Get an iterator and pull the first value.
    it = iter(iterable)
    last = next(it)
    # Run the iterator to exhaustion (starting from the second value).
    for val in it:
        # Report the *previous* value (more to come).
        yield last, True
        last = val
    # Report the last value.
    yield last, False


def getMyTitleKey(title):
    title = title.lower()
    #print(title)
    #print("<br>")
    if title == 'the computational complexity of finding separators in temporal graphs.':
        return "the complexity of finding small separators in temporal graphs."
    if title == 'facility location under matroid constraints - fixed-parameter algorithms and applications.':
        return "fixed-parameter algorithms for maximum-profit facility location under matroid constraints."
    #if title == 'multistage s-t path - confronting similarity with dissimilarity.':
    #    return "multistage s-t path - confronting similarity with dissimilarity in temporal graphs."
    if title == 'multistage s-t path - confronting similarity with dissimilarity in temporal graphs.':
        return "multistage s-t path - confronting similarity with dissimilarity."
    if title == 'the computational complexity of finding temporal paths under waiting time constraints.':
        return "finding temporal paths under waiting time constraints."
    return title    






