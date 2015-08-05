#!/usr/bin/env python3

import sys
import os.path
import urllib.request
from pyquery import PyQuery as pq

totalDownload = 0

def downloadFile(url,fileName):
    global totalDownload
    print("Downloading: " + fileName)
    file = urllib.request.urlretrieve(url, fileName)
    totalDownload += int(file[1]["Content-Length"])
    print("Downloaded: " + fileName + " " + file[1]["Content-Length"] + " bytes")

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
try:
    d = pq(url, headers={'user-agent': 'pyquery'})
except UnboundLocalError:
    exit("Network error")

elements = d(".fileText a")
links = []
for element in elements:
    links.append({'name': pq(element).html(), 'url': pq(element).attr("href")})

if (filter != ""):
    links = filterLinks(links, filter)

total = len(links)
if total == 0:
    exit("Nothing found - Bye")

print("Found " + str(total) + " resources.")

# Download links
for i, link in enumerate(links, start=1):
    print("File "+ str(i) + " of " + str(total) + " - " + str(round(((i / total) * 100.0),2)) + "%")
    if not os.path.exists(link["name"]):
        downloadFile(link["url"].replace("//", "http://"), link["name"] )
    else:
        print("Already downloaded")

exit("All files Downloaded! " + str(round((totalDownload / 1024 / 1024),2)) + "Mb")
