# 4download
Download all files like images, videos from a thread in [4chan](http://www.4chan.org/)

    Usage: 4download [-h] -u URL [-f FILTERS [FILTERS ...]] [-d DELAY]

## Requirements

  + [Python3](https://www.python.org/download/releases/3.0/)
  + [pyquery](https://pypi.python.org/pypi/pyquery)

```
sudo apt-get install python3
sudo pip3 install pyquery
```

## Examples

Download all resources in the thread

    4download -u http://boards.4chan.org/g/thread/39894014

Download all png, webm files

    4download -u http://boards.4chan.org/g/thread/39894014 -f png webm

Check the web page every minute for new resources

    4download -u http://boards.4chan.org/g/thread/39894014 -d 1

## Remember

Never abuse with this type of software, we have a nice community here, we don't want to ruin it.

![Pepe](pepe.gif)
