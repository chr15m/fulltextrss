# RSSFilter - Fetch, Parse, Filter and Re-Feed RSS
by Cathal Garvey, Copyright 2015, licensed under the [GNU Affero GPL](https://gnu.org/licenses/agpl.txt).

## What it does
RSSFilter lets you take an RSS feed, apply regex queries (or custom-defined functions)
to the feed, and then present the result as a new RSS feed ready for consumption by a
feed reader. It has an entry point for terminal usage, and is well suited (indeed,
developed for) for integration in a simple web-app relay.

## Why I wrote it
I'm mulling the problem of mass-data-funnelling a lot lately and this is just one experiment
as part of a much broader thing. Specifically this was inspired by the annoying discovery
of a news website that provided an RSS feed for *all* news but not for topic-specific
news. Thankfully, the topics had appropriate URL paths, so the science news could
be filtered by selecting articles containing "/science/" in them. So was born RSSFilter.

## Usage
Install: `sudo pip install rssfilter` (or sudo python3 setup.py install)

Installation gives you the rssfilter module, and also the rssfilter terminal
tool.

Included in the git repo is a trivial example usage for a Flask webapp, but this
is not installed with rssfilter when pip-installed or similar.

As currently written the entry-points accept up to two filters which may contain
arbitrary regex expressions. As there are only two built-in filter-classes this
two-filter limit isn't really a limit at all. There is an option whether to combine
the given two filters by boolean AND or OR.

In module usage you can define your own filters; they should accept a feed in
a format as returned by feedparser (but with all elements converted to native
types!) and return one in the same format.

## Example Terminal Usage:

Fetching recent articles on the Marriage Equality referendum in Ireland (May 2015) from
the Irish Times RSS feed:

    rssfilter https://www.irishtimes.com/cmlink/the-irish-times-news-1.1319192 -t '([Gg]ay|[Hh]omosexual|[Mm]arriage|[Rr]eferend)'

(Use 'rssfilter --help' for more information)
    
Importing and using the module to achieve the same result:

    import rssfilter
    it_feed = "https://www.irishtimes.com/cmlink/the-irish-times-news-1.1319192"
    f = rssfilter.filter_feed(it_feed, rssfilter.in_title_filter('([Gg]ay|[Hh]omosexual|[Mm]arriage|[Rr]eferend)'))
    print(f)

To learn more, read the source code docstrings or use iPython to explore with the "?"
appellation.
