#!/usr/local/bin/python

from SimpleXMLRPCServer import SimpleXMLRPCServer
import socket, time, pickle
import os, os.path
import random, md5

destdir = "/var/webarchive/crawler/urlstodo"
formmaildestdir = "/var/db/formmail"

if not os.path.exists(destdir):
    os.makedirs(destdir)
if not os.path.exists(formmaildestdir):
    os.makedirs(formmaildestdir)



def submit_formmail(source, data):
    if 'form.p' in data:
	data['form'] = pickle.loads(data['form.p'])
	del data['form'] 
    fn = os.path.join(formmaildestdir, "%s-%d-%f.p" % (source, os.getpid(), time.time()))
    fd = open("%s" % fn, "w")
    pickle.dump(data, fd)
    fd.close()
    return "Ok"


def submit_new_urls(uid, l):
    # we don't use a timestamp directly to incerase submitter privacy
    uid = md5.new("%f %d %f" % (time.time(), os.getpid(), random.random())).hexdigest()
    print uid
    fn = os.path.join(destdir, "%s.newurls" % (uid))
    fd = open("%s.tmp" % fn, "w")
    print "writing"
    fd.write("\n".join([x.data for x in l]))
    print "closing"
    fd.close()
    print 'os.rename("%s.tmp", %r)' % (fn, fn)
    os.rename("%s.tmp" % fn, fn)
    # obfuscate file time to incerase submitter privacy
    t = time.time() - (random.random() * 60 * 60 * 24 * 5)
    print "utime(%r)" % t
    os.utime(fn, (t, t)) 
    return "Ok"

server = SimpleXMLRPCServer(("b.23.nu", 8000))
server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
server.register_function(submit_new_urls)
server.register_function(submit_formmail)
server.serve_forever()    
