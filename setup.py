#!/usr/bin/env python

from setuptools import setup

setup(
    name='fulltextrss',
    version='0.0.1',
    description='Re-render RSS feeds with full-text articles.',
    author='Chris McCormick',
    author_email='chris@mccormick.cx',
    keywords=('rss', 'atom', 'feed', 'subscription', 'filter', 'fulltextrss', 'web', 'news'),
    license = "AGPL",
    entry_points = {
        "console_scripts": [
            'fulltextrss = fulltextrss:_cli_main'
        ]
    },
    exclude_package_data={'': ['.gitignore']},
    packages=['fulltextrss'],
    requires=['feedgenerator', 'feedparser', 'bs4', 'lxml', 'newspaper'],
    install_requires=['feedgenerator', 'feedparser', 'bs4', 'lxml', 'newspaper'],
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
    long_description = open('README.md').read(),
    url='http://github.com/chr15m/fulltextrss'
)
