#!/usr/bin/python

datadirs = ["data"]

from marshal import dump, load

import os, os.path, time
from ARCive import ARCive

from pprint import pprint

dbDir = {}

def createDatabaseFromScratch():
    global dbDir
    dbDir = {}
    for d in datadirs:
        for basefn in os.listdir(d):
            fn = os.path.join(d, basefn)
            if os.path.isfile(fn) and fn.endswith(".arc"):
		arcDir = arcDirGetCacheForDb(d, basefn)
		if not arcDir:
                    a = ARCive(fn, 'r')
                    arcDir = a.getDir()
                    saveCacheForDb(arcDir, d, basefn)
                for url in arcDir:
                    if url not in dbDir:
                        dbDir[url] = []
                    for x in arcDir[url]:
                        dbDir[url].append((x["checksum"], x["date"], x["offset"], fn))

def saveCacheForDb(arcDir, d, basefn):
    if not os.path.exists(os.path.join(d, ".cache")):
        os.makedirs(os.path.join(d, ".cache"))
    fn = os.path.join(d, ".cache", basefn)
    fd = open("%s.marshal" % fn, "w")
    dump(arcDir, fd)
    fd.close()

def arcDirGetCacheForDb(d, basefn):
    cachn = "%s.marshal" % os.path.join(d, ".cache", basefn)
    arcn = os.path.join(d, basefn)
    if os.path.exists(cachn) and os.path.exists(arcn) and \
       (os.path.getmtime(cachn) >= os.path.getmtime(arcn)):
        return load(open(cachn)) 
    else:
        return None
	
def updateMemoryDb():
    if dbDir == {}:
        createDatabaseFromScratch()

def getEntries(url):
    updateMemoryDb()
    if url in dbDir:
        return dbDir[url]
    else:
        return None

def getURLsBySubstring(urlfragment):
    updateMemoryDb()
    ret = []
    for x in dbDir.keys():
        if urlfragment in x:
            ret.append(x)
    return ret

def getFile(pos, file, url):
    print url, pos, file
    a = ARCive(file)
    ret = a.readRawDocAtPos(pos)
    a.close()
    return ret

def getURLs():
    updateMemoryDb()
    return dbDir.keys()

if __name__ == "__main__":
    pprint(getEntries("http://blogs.23.nu/"))
    getEntries("http://blogs.23.nu/")

    print len(dbDir.keys())
    #pprint(dbDir)

    
