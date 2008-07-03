#!/usr/bin/env python
# encoding: utf-8
"""
extractor.py

Created by Maximillian Dornseif on 2008-06-28.
Copyright (c) 2008 HUDORA. All rights reserved.
"""

# contains code from the eff-bot archives:
# extract anchors from an HTML document
# fredrik lundh, may 1999
# fredrik@pythonware.com
# http://www.pythonware.com

import sys
import os
import unittest
import htmllib
import formatter
import urlparse
import string
import re
import urllib2, htmldata
from BeautifulSoup import BeautifulSoup          # For processing HTML

class myParser(htmllib.HTMLParser):
    def __init__ (self, base):
        htmllib.HTMLParser.__init__(self, formatter.NullFormatter())
        self.anchors = []
        self.base = base
    
    def anchor_bgn(self, href, name, type):
        self.save_bgn()
        if self.base:
            self.anchor = urlparse.urljoin(self.base, href)
        else:
            self.anchor = href
    
    def anchor_end(self):
        text = string.strip(self.save_end())
        if self.anchor and text:
            self.anchors.append((self.anchor, text))


href_re = re.compile(r'''href=[ "']*([^ "'#]+)[ "']+>([^<]+)''', re.DOTALL|re.IGNORECASE)
src_re = re.compile(r'''(href|src)=[ "']*([^ "'#]+)[ "']+[^>]*>''', re.DOTALL|re.IGNORECASE)
http_re = re.compile(r'''[ "']*(http://[^ "'#]+)[ "']>''', re.DOTALL|re.IGNORECASE)
def parse_for_links(data, url):
    ret = set()
    for link, text in re.findall(href_re, data):
        if link.startswith('http://'):
            ret.add((link, text))
        else:
            ret.add((urlparse.urljoin(url, link), text))
    
    for dummy, link in re.findall(src_re, data):
        if link.startswith('http://'):
            ret.add((link, ''))
        else:
            ret.add((urlparse.urljoin(url, link), link))
    
    for link in re.findall(http_re, data):
        ret.add((link, ''))
    
    if len(ret) < 1:
        print len(ret), len(data)
        print list(ret)
        print repr(data[:30])
        print '\n\n\n\n\n'
    return list(ret)


def extract_links(url, ref):
    global urlcount
    print '->', url, ref
    socket.timeout = 120
    h = httplib2.Http()
    try:
        resp, content = h.request(url, 'GET', headers={'Referer': ref, # 'Range': 'bytes=bytes=10000',
                                                   'User-Agent': 'AltaVista II Crawler'})
        urlcount += 1
    except TypeError:
        return []
    except httplib2.RelativeURIError:
        return []
    except httplib2.ServerNotFoundError:
        return []
    except socket.error:
        return []
    else:
        # write to archive
        arc.writeRawDoc(content, url)
    # extract links and return them
    return parse_for_links(content, url)
