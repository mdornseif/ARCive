#!/usr/bin/env python
# encoding: utf-8
"""
test.py

Created by Maximillian Dornseif on 2008-06-05.
Copyright (c) 2008 HUDORA. All rights reserved.
"""

import random
import urllib
import time
import tools


searchterms = tools.terms_from_file('terms/companies.txt')
searchterms.extend(tools.terms_from_file('terms/products.txt'))
searchengines = tools.read_list('terms/searchengines.txt')

print len(searchterms)*len(searchengines)

def urls_for_searchengines(searchterm):
    for engineurl in searchengines:
        yield engineurl.replace('XXX', urllib.quote_plus(searchterm))

ret = []

for term in searchterms:
    ret.extend(urls_for_searchengines(term))

print len(ret)
random.shuffle(ret)
print len(ret)
time.sleep(100000)
