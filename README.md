A simple command line utility for turning RSS feeds with partial content into full-content feeds.

	curl https://www.sciencemag.org/rss/news_current.xml | fulltextrss > sciencemag-news-full-text.xml

Install:

	pip install --user -e git+https://github.com/chr15m/fulltextrss.git#egg=fulltextrss

Derived from [RSSFilter](https://github.com/cathalgarvey/rssfilter) by Cathal Garvey, Copyright 2015, licensed under the [GNU Affero GPL](https://gnu.org/licenses/agpl.txt).

See [original-readme.md](./original-readme.md) for more information.
