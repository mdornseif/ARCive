#!/usr/bin/python

# containsvfrom the eff-bot archives:
# extract anchors from an HTML document
# fredrik lundh, may 1999
# fredrik@pythonware.com
# http://www.pythonware.com

import htmllib
import formatter
import string
import urllib, urlparse
import httplib
import re
import signal
import time, random

import httplib2

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

def parse_for_links(data, url):
    p = myParser(url)
    try:
        p.feed(data)
        p.close()
        return [x[0] for x in p.anchors]
    except (AttributeError, htmllib.HTMLParseError):
        print "parse error for %r" % url
        return []

def extract_links(url, ref):
    print url, ref
    h = httplib2.Http(".cache")
    # first ensure that the internet archive knows about this site
    resp, content = h.request('http://web.archive.org/web/*/'+url)
    resp, content = h.request(url, 'GET', headers={'Referer': ref, # 'Range': 'bytes=bytes=10000',
                                                   'Accept-Encoding': 'gzip, compress',
                                                   'User-Agent': 'iCab/2.8.1 (Macintosh; I; PPC; Mac OS X; kiesel)'})
    return parse_for_links(content, url)

def spider(seeds):
    def ALRMhandler(signum, frame):
        print 'Signal handler called with signal', signum

    def INFOhandler(signum, frame):
        print "current frontier: %d, new frontier %d, dupes %d, current depth: %d" % (len(frontier), len(newfrontier), len(dupelist), page['level'])
   
    signal.signal(signal.SIGINFO, INFOhandler)
    # signal.signal(signal.SIGALRM, signal.SIG_IGN)
    signal.signal(signal.SIGALRM, ALRMhandler)
    
    dupelist = set()
    frontier = []
    for seedurl in seeds:
        frontier.append(dict(url=seedurl, ref='', level=0))
    
    while frontier:
        random.shuffle(frontier)
        newfrontier = []
        print "processing frontier with %d urls" % len(frontier)
        for page in frontier:
            if page['url'] in dupelist:
                continue
            links = extract_links(page['url'], page['ref'])
            dupelist.add(page['url'])
            if links and page['level'] < 2:
                for link in links:
                    if page['url'] in link and link not in dupelist:
                        newfrontier.append(dict(url=link, ref=page['url'], level=page['level']+1))
                    if page['level'] > 0 and link not in dupelist:
                        newfrontier.append(dict(url=link, ref=page['url'], level=page['level']+1))
        print len(newfrontier)
        frontier = newfrontier[:]
        print len(frontier)

spider(['http://blogs.23.nu/c0re/',
        'http://blogs.23.nu/disLEXiaDE/',
        'http://blogs.23.nu/demagoge/',
        'http://blogs.23.nu/just/',
        'http://blogs.23.nu/bubbleboy/',
        'http://blogs.23.nu/nnbon/',
        'http://technorati.com/blogs/blogs.23.nu/c0re?reactions',
        'http://technorati.com/blogs/blogs.23.nu/disLEXiaDE?reactions',
        'http://www.hudora.de/unternehmen/jobs/freelancing/',
        #'http://technorati.com/posts/tag/hudora',
        #'http://search.yahoo.com/search?p=hudora',
        #'http://search.lycos.com/default.asp?query=hudora',
        #'http://www.ask.com/web?q=hudora',
        #'http://www.alltheweb.com/search?cat=web&q=hudora',
        #'http://www.google.de/products?q=hudora&btnG=Produkte+suchen',
        #'http://www.altavista.com/web/results?q=hudora',
        #'http://vivisimo.com/search?query=hudora',
        #'http://www.a9.com/hudora',
])

if __name__  == '__main__S':
    def ALRMhandler(signum, frame):
        print 'Signal handler called with signal', signum
    signal.signal(signal.SIGALRM, ALRMhandler)

    
