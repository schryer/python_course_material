#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'David Schryer'
SITENAME = u'Scientific Programming with Python'
SITEURL = 'python_course_material'
TYPOGRIFY = True

CUSTOM_ARTICLE_SHARING = 'sharing.html'
CUSTOM_ARTICLE_SCRIPTS = 'sharing_scripts.html'

TIMEZONE = 'Europe/Tallinn'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

#THEME = 'pelican-themes/subtle'
THEME = 'pelican-themes/bootstrap2'

#from plugins.pelican_plugin_render_math import math
#PLUGINS = [math,]

#MARKUP = ('md', 'ipynb')
PLUGIN_PATHS = ['pelican-plugins',]
PLUGINS = ['render_math']
