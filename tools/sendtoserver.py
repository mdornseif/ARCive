#!/usr/bin/python

# problem: http://211.78.96.5/vip/coffee/\xb6g\xa6~\xbcy\xac\xa1\xb0\xca2.GIF

# sends a list of URLs read from stdin to our Arcive server.

import  xmlrpclib
import sys

server =  xmlrpclib.ServerProxy("http://b.23.nu:8000", verbose=0,)

urls = []

for x in sys.stdin.readlines():
    urls.append(xmlrpclib.Binary(unicode(x.strip(), 'utf-8', 'replace').encode('ascii', 'replace')))
    if len(urls) > 1237:
        server.submit_new_urls("", urls)
        urls = []

print "last batch", len(urls)
server.submit_new_urls("", urls)

