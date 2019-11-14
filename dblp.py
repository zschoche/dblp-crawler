import urllib.request
import collections
import json

def printPub(paper):
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
    if title == 'the computational complexity of finding separators in temporal graphs.':
        return "the complexity of finding small separators in temporal graphs."
    if title == 'facility location under matroid constraints - fixed-parameter algorithms and applications.':
        return "fixed-parameter algorithms for maximum-profit facility location under matroid constraints."
    return title    


page = urllib.request.urlopen('https://dblp.org/search/publ/api?q=author%3APhilipp%20Zschoche%3A&format=json')
result = json.loads(page.read().decode("utf8"))
papers = {}
for x in result['result']['hits']['hit']:
  paper = x['info']
  title = getMyTitleKey(paper['title'])
  if title in papers:
    papers[title].append(paper)
  else:
    papers[title] = [paper]

year = '0'
for key in papers:
  paper = papers[key][0]
  if year != paper['year']:
      year = paper['year']
      print("<h1>" + year + "</h1>")
  else:
      print()


  for author, more in lookahead(paper['authors']['author']):
      if more:
        print(author, end =", "),
      elif len(paper['authors']['author']) == 1:
          print(author,":"),
      else:
        print('and', author,end=":<br>\n")
  last = " "
  if 'pages' in paper:
      last = ": "

  print("<b>" + paper['title']+ "</b><br>")
  for pub, morepub in lookahead(papers[key]):
      print("<a href='" + pub["ee"] + "'>")
      printPub(pub)
      print("</a>")
      if morepub:
        print("&nbsp;|&nbsp;")
  print("<br><br>")


      


