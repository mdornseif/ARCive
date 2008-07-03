#!/usr/bin/env python
# encoding: utf-8
"""
frontier.py

Created by Maximillian Dornseif on 2008-06-28.
Copyright (c) 2008 HUDORA. All rights reserved.
"""

import sys
import md5
import urlparse
import urllib
import random
import bsddb
from tools import tools

# we use 256 wueues hased by hostname
queues = []
currentqueue = 0
for i in range(256):
    queues.append([])
    
dupes = bsddb.btopen('./dupes', 'w')

def add(url, priority=False):
    # normalize url, remove fragment
    (scheme, location, path, query, fragment) = urlparse.urlsplit(url)
    url = urlparse.urlunsplit((scheme, location, path, query, ''))
    if dupes.has_key(url):
        return
    dupes[url] = 'T'
    queid = ord(md5.new(location).digest()[0])
    if priority:
        queues[queid].insert(0, x)
    else:
        queues[queid].append(url)

def get():
    global currentqueue
    count = 0
    while not len(queues[currentqueue]) and count < len(queues)+1:
        currentqueue += 1
        currentqueue %= len(queues)
        count += 1
    ret = queues[currentqueue].pop(0)
    currentqueue += 1
    currentqueue %= len(queues)
    return ret
    
def show():
    print [len(x) for x in queues]
    print sum([len(x) for x in queues])

def init():
    starturls = tools.read_list('tools/starturls-fixed.txt')
    searchterms = tools.terms_from_file('tools/terms/companies.txt')
    searchterms.extend(tools.terms_from_file('tools/terms/products.txt'))
    searchengines = tools.read_list('tools/terms/searchengines.txt')

    def urls_for_searchengines(searchterm):
        random.shuffle(searchengines)
        for engineurl in searchengines:
            yield engineurl.replace('XXX', urllib.quote_plus(searchterm))
    
    random.shuffle(searchterms)
    for searchterm in searchterms:
        urls = list(urls_for_searchengines(searchterm))[:3]
        random.shuffle(urls)
        starturls.extend(urls)
    random.shuffle(searchterms)
    for url in starturls:
        add(url)
    show()