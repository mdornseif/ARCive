import pcap, time, sys

p = pcap.pcapObject()
net, mask = pcap.lookupnet("xl1")
p.open_live("xl1", 1600, 0, 100)
p.setfilter("tcp port 80 or port 8080 or port 3128" , 0, 0)

dupecache = {}

def print_deduped(data):
    if data not in dupecache:
        print data
        sys.stdout.flush()
    dupecache[data] = time.time()


def print_packet(pktlen, data, timestamp):
    if not data or pktlen > 1400:
        return
    # remove minimum IP / TCP header
    data = data[54:]
    pos = data.find("GET")
    if pos < 0:
        pos = data.find("HEAD")
    if pos < 0:
        return
    data = data[pos:]
    l = data.split("\n")
    reqstr = l[0]
    reqstr = reqstr[reqstr.find(" ")+1:reqstr.rfind(" ")]
    if reqstr[:1] != "/":
        reqstr = "/%s" % reqstr
    host = referer = None
    for x in l:
        if x.startswith("Host: "):
           host = x[6:].strip()
        if x.startswith("Referer: "):
           referer = x[9:].strip()
    if not reqstr.endswith(".gif") and not reqstr.endswith(".jpg") and \
        not reqstr.endswith("css") and not reqstr.endswith("js") and \
        not reqstr.endswith("swf"):
        print_deduped("http://%s%s" % (host, reqstr))
    if referer:
        print_deduped(referer)

while 1:
    p.loop(1, print_packet)
