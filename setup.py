#!/usr/bin/env python

from setuptools import setup

setup(
    name='rssfilter',
    version='0.0.1',
    description='Fetch, filter, and re-render RSS feeds for more useful consumption.',
    author='Cathal Garvey',
    author_email='cathalgarvey@cathalgarvey.me',
    keywords=('rss', 'atom', 'feed', 'subscription', 'filter', 'regex', 'web', 'news'),
    license = "AGPL",
    entry_points = {
        "console_scripts": [
            'rssfilter = rssfilter:_cli_main'
        ]
    },
    exclude_package_data={'': ['.gitignore']},
    packages=['rssfilter'],
    requires=['feedgenerator', 'feedparser', 'bs4', 'lxml'],
    classifiers= [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Text Processing',
    'Topic :: Utilities'],
    long_description = open('ReadMe.md').read(),
    url='http://github.com/cathalgarvey/rssfilter'
)
