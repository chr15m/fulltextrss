#!/usr/bin/env python3
"""An RSS filtering tool/library that helps you to take a feed, apply some custom-defined parameters or filtering functions, and generate a valid filtered feed for consumption in a normal RSS reader. In terminal usage this prints the generated feed (pretty-printed)."""

import time
import datetime
import re
import copy
import sys
import urllib2

import bs4
import feedgenerator
import feedparser
from newspaper import fulltext

class FeedFetchError(Exception):
    "Thrown when something goes awry fetching or parsing the original feed."
    pass

class FeedFilterError(Exception):
    "Thrown when invalid filter data are given or something blows up when executing filtration."
    pass

def _cast_feed_to_primitives(feed):
    """
    Feedparser's Dicts have lots of peculiar bugs: They present certain keys as
    existing, but they are not poppable, and they don't do **unpacking well. So,
    this converts all the relevant values to dict primitives so they can be expected
    to behave in the usual way. This is called by filter_feed for *all* feeds
    generated by feedparser.
    """
    feed = dict(feed)
    feed['feed'] = dict(feed['feed'])
    for k,v in feed['feed'].items():
        if isinstance(v, feedparser.FeedParserDict):
            feed['feed'][k] = dict(v)
    nuentries = []
    for i in feed['entries']:
        i = dict(i)
        for k,v in i.items():
            if isinstance(v, feedparser.FeedParserDict):
                i[k] = dict(v)
        nuentries.append(i)
    feed['entries'] = nuentries
    return feed

def fetch_and_prepare_feed(feed_url=None):
    """
    Makes the HTTP requests to get a feed and parses them with feedparser.
    
    Further modifies things so the returned feed doesn't consist of or contain
    feedparser types, to avoid cryptic downstream bugs (looks-like-a-dict-but-acts-funny).
    Also adds a key (if not already there) 'pubdate' to each given RSS item based
    on feedparser's 'published_parsed' struct_time item. 'pubdate' is a datetime.datetime
    object, as required by feedgenerator.
    """
    f = feedparser.parse(feed_url or sys.stdin)
    if feed_url and (not f['feed'] or not (200 <= f['status'] < 300)):
        raise FeedFetchError()
    f = _cast_feed_to_primitives(f)
    for i in f['entries']:
        if not isinstance(i.get('pubdate', None), datetime.datetime):
            i['pubdate'] = datetime.datetime.fromtimestamp(time.mktime(i.get('published_parsed', i.get('updated_parsed', datetime.datetime.now()))))
    return f

def builtin_main(feed_url):
    """Accepts a feed URL and adds full-content to each entry."""
    f = fetch_and_prepare_feed(feed_url)
    if not f['feed'].get('description', None):
        if f['feed']['title']:
            f['feed']['description'] = f['feed']['title']
        elif f['feed']['link']:
            f['feed']['description'] = f['feed']['link']
        else:
            f['feed']['description'] = "Unknown title"
    title = f['feed'].pop('title')
    link = f['feed'].pop('link')
    description = f['feed'].pop('description')
    o = feedgenerator.Rss201rev2Feed(title, link, description, **f['feed'])
    for i in f['entries']:
        url = i["link"]
        # if we're looking at a reddit site ignore their
        # broken link structure and use their [link] link (*facepalm*)
        if "reddit.com/r/" in link:
            original_html = i.get("description", None) or i.get("summary", None)
            s = bs4.BeautifulSoup(original_html)
            for a in s.find_all('a', href=True):
                if a.contents == [u"[link]"] and a.get("href") and not (a.get("href").lower().endswith(".png") or a.get("href").lower().endswith(".gif") or a.get("href").lower().endswith(".jpg")):
                    url = a.get("href")
                    break
        if url:
            # fake our user agent because some sites are crybabies
            req = urllib2.Request(url, None, {'User-Agent': 'Mozilla/5.0'})
            html = urllib2.urlopen(req).read()
            if html:
                try:
                    i["description"] = fulltext(html)
                except:
                    sys.stderr.write("Unable to parse: %s\n" % url)
                else:
                    try:
                        o.add_item( **i )
                    except:
                        sys.stderr.write("Unable to add: %s\n" % url)
            else:
                sys.stderr.write("Unable to fetch: %s\n" % url)
    feedstr = o.writeString("utf-8")
    feedstr = bs4.BeautifulSoup(feedstr, 'xml').prettify().encode("utf-8", "ignore")
    return feedstr

def _cli_main():
    import argparse
    P = argparse.ArgumentParser(description=__doc__)
    P.add_argument("source", type=str, help="Target feed to fetch and apply filters to.", default=None, nargs='?')
    A = P.parse_args()
    print(builtin_main(A.source))

if __name__ == "__main__":
    _cli_main()
