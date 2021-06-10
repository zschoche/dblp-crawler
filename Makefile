all:
	python3 dblp.py&

check: all open


open:
	python3 dblp.py > tmp.html
	google-chrome tmp.html

news:
	python3 news.py > tmp.html
	google-chrome tmp.html


