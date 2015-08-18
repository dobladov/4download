#!/usr/bin/env python3

import argparse
import os.path
import urllib.request
from threading import Timer
from pyquery import PyQuery as pq

totalDownload = 0
totalFiles = 0


def parseArgs():
    parser = argparse.ArgumentParser(description='Download all images, videos'
                                                 + ' from a thread in 4chan')
    parser.add_argument('-u',
                        '--url',
                        type=str,
                        required=True,
                        help='url of the thread')
    parser.add_argument('-f',
                        '--filters',
                        type=str,
                        help='file format',
                        nargs='+')
    parser.add_argument('-d', '--delay', type=int, help='fech time in minutes')

    return parser.parse_args()


def getLinks(url, filters):
    global totalFiles

    try:
        content = pq(url, headers={'user-agent': 'pyquery'})
    except UnboundLocalError:
        exit("Network error")

    elements = content(".fileText a")
    links = []
    for element in elements:
        links.append({'name': pq(element).html(),
                      'url': pq(element).attr("href")})

    if filters:
        links = filterLinks(links, filters)

    if len(links) == 0:
        exit("Nothing found - Bye")
    elif len(links) == totalFiles:
        print("Nothig New")
        return None
    elif totalFiles < len(links):
        if (totalFiles == 0):
            totalFiles = len(links)
            print("Found " + str(totalFiles) + " resources.")
            return links
        else:
            temp = totalFiles
            print(str(len(links)-totalFiles) + " New files")
            totalFiles = len(links)
            return links[temp:]


def downloadLinks(links):
    for i, link in enumerate(links, start=1):
        print("File " + str(i) + " of " + str(len(links)) + " - "
              + str(round(((i / len(links)) * 100.0), 2)) + "%")
        if not os.path.exists(link["name"]):
            downloadFile(link["url"].replace("//", "http://"), link["name"])
        else:
            print("Already downloaded")

    totalMb = round((totalDownload / 1024 / 1024), 2)
    print("%d file%s Downloaded! %.2fMb" % (totalFiles,
          "s"[totalFiles == 1:], totalMb))


def downloadFile(url, fileName):
    global totalDownload
    print("Downloading: " + fileName)
    file = urllib.request.urlretrieve(url, fileName)
    totalDownload += int(file[1]["Content-Length"])
    print("Downloaded: " + fileName + " " + file[1]["Content-Length"]
          + " bytes")


def filterLinks(urls, filters):
    result = []
    for url in urls:
        if url["url"].split("/")[-1].split(".")[-1] in filters:
            result.append(url)
    return result


def main():
    args = parseArgs()
    links = getLinks(args.url, args.filters)
    if links:
        downloadLinks(links)

    if args.delay:
        print("Checking again in %d minute%s"
              % (args.delay, "s"[args.delay == 1:]))
        Timer(args.delay*60, main).start()

if __name__ == "__main__":
    main()
