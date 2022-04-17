import requests
import csv
from bs4 import BeautifulSoup
import re
import sys


urls = dict()

with open('data.csv', newline='') as f:
    reader = csv.DictReader(f)

    for row in reader:
        urls[row['link']] = list()

    print('foram encontradas %i urls' % len(urls.keys()))

for url in urls.keys():
    try:
        print('coletando as tags do video: %s' % url)
        r = requests.get(url)
    except:
        continue

    soup = BeautifulSoup(r.content, features="lxml")

    for link in soup.findAll("a", attrs={"class": "text-tui-sm"}):
        text = link.findNext('a').text

        # ignorar categoria que inicei com TED
        if not text.lower().startswith('ted'):
            urls[url].append(text)

with open('tags.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['url', 'tag'])
    writer.writeheader()

    for url in urls.keys():
        for tag in urls[url]:
            writer.writerow({'url': url, 'tag': tag})
