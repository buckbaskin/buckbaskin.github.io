#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

PLUGIN_PATHS = ['./custom/']
PLUGINS = ['latex2mathml_reader',]

AUTHOR = 'Buck Baskin'
SITENAME = 'Building and Breaking'
SITESUBTITLE = ''
SITEURL = '/blog'
THEME = 'themes/simple'

PATH = 'site'
STATIC_PATHS = ['img']

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_DOMAIN = 'https://buckbaskin.com/blog'
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
FEED_ALL_RSS = 'feed'

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.toc': {
            'permalink': True,
        },
    }
}

DIRECT_TEMPLATES = ['index', 'tags', 'archives', 'projects']
