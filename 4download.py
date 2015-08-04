#!/usr/bin/env python3

import sys
import urllib.request
from pyquery import PyQuery as pq

def downloadFile(url):
    file_name = url.split('/')[-1]
    print("Downloading: "+ file_name)
    file = urllib.request.urlretrieve(url, file_name)
    print("Downloaded: "+file[0]+ " " + file[1]["Content-Length"] + " bytes")

def filterLinks(urls, filter):
    result = []
    for url in urls:
        if url.split("/")[-1].split(".")[-1] == filter:
            result.append(url)
    return result

try: # URL Argument
    url = sys.argv[1]
except IndexError:
    exit("Usage: 4download url [filter]")

try: # Filter argument
    filter = sys.argv[2]
except IndexError:
    filter = ""

## Get URLs
d = pq(url, headers={'user-agent': 'pyquery'})
elements = d(".fileText a")
links = []
for element in elements:
    links.append(pq(element).attr("href"))

if (filter != ""):
    links = filterLinks(links, filter)

total = len(links)
if total == 0:
    exit("Nothing found - Bye")

print("Found " + str(total) + " resources.")

#Descargar enlaces
for i, link in enumerate(links, start=1):
    print("File "+ str(i) + " of " + str(total))
    downloadFile(link.replace("//", "http://"));
exit("All files Downlaoded!")
