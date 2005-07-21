#!/usr/bin/python

#from the eff-bot archives:
#
# extract anchors from an HTML document
#
# fredrik lundh, may 1999
#
# fredrik@pythonware.com
# http://www.pythonware.com
#

import htmllib
import formatter
import string
import urllib, urlparse
import httplib
import re
import signal
import time, random

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

if __name__  == '__main__':

    def ALRMhandler(signum, frame):
        print 'Signal handler called with signal', signum
        
    URLs = ['http://md.hudora.de/publications/',
            'http://md.hudora.de/presentations/',
	    #'http://blogs.23.nu/disLEXia/',
            'http://blogs.23.nu/c0re/',
	    #'http://blogs.23.nu/devconxi/',
            #'http://blogs.23.nu/netzzensur/',
            #'http://blogs.23.nu/rade/',
	    #'http://blogs.23.nu/jurtex/',
            #'http://blogs.23.nu/inbox/'
            #'http://blogs.23.nu/dabringhausen/',
            #'http://blogs.23.nu/datenmuell/',
            #'http://blogs.23.nu/netzzensur/referrers',
            #'http://blogs.23.nu/disLEXia/referrers',
            #'http://blogs.23.nu/just/',
            #'http://blogs.23.nu/demagoge/',
            #'http://blogs.23.nu/cybercrime/referrers',
            #'http://blogs.23.nu/fsck/',
            #'http://blogs.23.nu/devconxi/',
            #'http://blogs.23.nu/RedTeam/',
            #'http://blogs.23.nu/antlab/',
            #'http://blogs.23.nu/rezepte/',
            #'http://blogs.23.nu/moe/',
            #'http://blogs.23.nu/RunningLAN/',
            'http://blogs.23.nu/disLEXiaDE/',
            #'http://blogs.23.nu/sevilla/',
            #'http://blogs.23.nu/lufgi4en/',
            'http://www-i4.informakik.rwth-aachen.de/lufg/', 
#'http://lufgi4.informatik.rwth-aachen.de/forms/listanswers/1',
'http://lufgi4.informatik.rwth-aachen.de/',
'http://lufgi4.informatik.rwth-aachen.de/staff',
'http://lufgi4.informatik.rwth-aachen.de/news',
'http://lufgi4.informatik.rwth-aachen.de/presentations',
'http://lufgi4.informatik.rwth-aachen.de/publications',
'http://lufgi4.informatik.rwth-aachen.de/conferences',
'http://lufgi4.informatik.rwth-aachen.de/cfps',
'http://lufgi4.informatik.rwth-aachen.de/calendar',
	]
    
    random.shuffle(URLs)
    ignore_re = re.compile('(mailto:|http://www-i4.informatik.rwth-aachen.de/|http://lufgi4.informatik.rwth-aachen.de/|http://blogs.23.nu/|http://md.hudora.de/|http://koeln.ccc.de/~drt|http://www.prognosisx.com|http://news.bbc.co.uk|http://www.newsisfree.com/|http://www.vnunet.com|http://www.theregister|http://radio.weblogs.com/0112292|http://radiocomments.userland.com/comments|http://radio.xmlstoragesystem.com/|http://(w)*.google|http://127.0.0.1)')

    signal.signal(signal.SIGALRM, ALRMhandler)
    dupes = {}
    for URL in URLs:
        print "***", URL
        try:
            f = urllib.urlopen(URL)

            p = myParser(URL)
            p.feed(f.read())
            p.close()

            random.shuffle(p.anchors)
            print p.anchors
            for x, foo in p.anchors:
                if not ignore_re.match(x):
                    if x not in dupes:
                        dupes[x] = None
                        try:
			    print x, URL
                            signal.alarm(120)
                            (proto, host, path, params, frag) = urlparse.urlsplit(x)
                            headers = {"Referer": URL,
				       "Accept-Encoding": 'gzip, compress',
                                       "User-Agent": 'iCab/2.8.1 (Macintosh; I; PPC; Mac OS X; kiesel)'}
                            conn = httplib.HTTPConnection(host)
                            conn.set_debuglevel(0)
                            if params:
                                path = path + '?' + params
                            if frag:
                                path = path + '#' + frag
                            conn.request("GET", path, None, headers)
                            response = conn.getresponse()
                            print response.status, response.reason
                            data = response.read()
                            conn.close()
                            time.sleep(random.randrange(3))
                            signal.alarm(0)

                            signal.alarm(60)
                            (proto, host, path, params, frag) = urlparse.urlsplit(x)
                            headers = {"Referer": 'http://blogs.23.nu/disLEXiaDE/stories/5890/',
				       "Accept-Encoding": 'gzip, compress',
                                       "User-Agent": 'iCab/2.8.1 (Macintosh; I; PPC; Mac OS X; kiesel)'}
                            conn = httplib.HTTPConnection(host)
                            #conn.set_debuglevel(9)
                            if params:
                                path = path + '?' + params
                            if frag:
                                path = path + '#' + frag
                            conn.request("GET", path, None, headers)
                            response = conn.getresponse()
                            #print response.status, response.reason
                            #data = response.read()
                            conn.close()
                            time.sleep(random.randrange(3))
                            signal.alarm(0)


                            signal.alarm(60)
                            (proto, host, path, params, frag) = urlparse.urlsplit(x)
                            headers = {"Referer": 'http://sauna.5711.org/~md/thumbnails/',
				       "Accept-Encoding": 'gzip, compress',
                                       "User-Agent": 'iCab/2.8.1 (Macintosh; I; PPC; Mac OS X; kiesel)'}
                            conn = httplib.HTTPConnection(host)
                            #conn.set_debuglevel(9)
                            if params:
                                path = path + '?' + params
                            if frag:
                                path = path + '#' + frag
                            conn.request("GET", path, None, headers)
                            response = conn.getresponse()
                            #print response.status, response.reason
                            #data = response.read()
                            conn.close()
                            time.sleep(random.randrange(3))
                            signal.alarm(0)

                        except:
                            print "das war nichts"
                            #raise
        except:
            print "das war nichts"
            #raise
                

    
