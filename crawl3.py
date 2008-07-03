#!/usr/bin/env python
# encoding: utf-8
"""
crawl3.py

Created by Maximillian Dornseif on 2008-06-28.
Copyright (c) 2008 HUDORA. All rights reserved.
"""

# based on retriever-multi.py,v 1.29 2005/07/28 11:04:13 mfx Exp

import sys
import os
import time
import pycurl
import ARCive
from cStringIO import StringIO
import extractor
import frontier

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 6.0)'

# We should ignore SIGPIPE when using pycurl.NOSIGNAL - see
# the libcurl tutorial for more info.
try:
    import signal
    from signal import SIGPIPE, SIG_IGN
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except ImportError:
    pass


frontier.init()

num_conn = 10
num_processed = 0
print "PycURL %s (compiled against 0x%x)" % (pycurl.version, pycurl.COMPILE_LIBCURL_VERSION_NUM)

# Pre-allocate a list of curl objects
m = pycurl.CurlMulti()
m.handles = []
for i in range(num_conn):
    c = pycurl.Curl()
    c.fp = None
    c.setopt(pycurl.USERAGENT, USER_AGENT)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5)
    c.setopt(pycurl.CONNECTTIMEOUT, 30)
    c.setopt(pycurl.TIMEOUT, 300)
    c.setopt(pycurl.NOSIGNAL, 1)
    #c.setopt(pycurl.COOKIEFILE, '')
    m.handles.append(c)

print 'ARCiving to %r' % ('spider-hudora-%s.arc.bz2' % time.strftime('%Y%m%d%H%M'))
arc = ARCive.ARCive('spider-hudora-%s.arc.bz2' % time.strftime('%Y%m%d%H%M'), 'w')

# Main loop
freelist = m.handles[:]
while True:
    # If there is an url to process and a free curl object, add to multi stack
    while freelist:
        url = frontier.get()
        c = freelist.pop()
        c.fp = StringIO()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.WRITEFUNCTION, c.fp.write)
        c.url = url
        m.add_handle(c)
    # Run the internal curl state machine for the multi stack
    while 1:
        ret, num_handles = m.perform()
        if ret != pycurl.E_CALL_MULTI_PERFORM:
            break
    # Check for curl objects which have terminated, and add them to the freelist
    while 1:
        num_q, ok_list, err_list = m.info_read()
        for c in ok_list:
            arc.writeRawDoc(c.fp.getvalue(), c.getinfo(pycurl.EFFECTIVE_URL))
            for link in extractor.parse_for_links(c.fp.getvalue(), c.getinfo(pycurl.EFFECTIVE_URL)):
                frontier.add(link[0])
            c.fp.close()
            c.fp = None
            m.remove_handle(c)
            print "Success:", c.url, c.getinfo(pycurl.EFFECTIVE_URL)
            freelist.append(c)
        for c, errno, errmsg in err_list:
            c.fp.close()
            c.fp = None
            m.remove_handle(c)
            print "Failed: ", c.url, errno, errmsg
            freelist.append(c)
        num_processed = num_processed + len(ok_list) + len(err_list)
        if num_q == 0:
            break
    # Currently no more I/O is pending, could do something in the meantime
    # (display a progress bar, etc.).
    # We just call select() to sleep until some more data is available.
    m.select(0.1)


# Cleanup
for c in m.handles:
    if c.fp is not None:
        c.fp.close()
        c.fp = None
    c.close()
m.close()
