#!/usr/bin/python
# -*- encoding: utf-8 -*-
# contains code from the eff-bot archives:
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
import socket
import threading

import httplib2

import ARCive
import tools

MAXLEVEL = 12
MAXTHREADS = 10
STARTTIME = time.time()
urlcount = 0

searchterms = tools.terms_from_file('terms/companies.txt')
searchterms.extend(tools.terms_from_file('terms/products.txt'))
searchengines = tools.read_list('terms/searchengines.txt')

linkterms = set()
for searchterm in searchterms:
    for term in searchterm.split():
        print term
        if len(term) > 4:
            linkterms.add(term)
linkterms = list(linkterms)
print len(linkterms)

def urls_for_searchengines(searchterm):
    random.shuffle(searchengines)
    for engineurl in searchengines:
        yield engineurl.replace('XXX', urllib.quote_plus(searchterm))


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
    ret = []
    try:
        # XML parser
        p.feed(data)
        p.close()
        for link, text in p.anchors:
            print repr((text, link))
            for searchterm in linkterms:
                if ((text+link).lower().find(searchterm) > -1 and link.startswith('http')) or not link.startswith('http'):
                    print searchterm,
                    print repr((text, link))
                    ret.append(link)
                    break # break out of inner loop
        return ret
    except (AttributeError, htmllib.HTMLParseError):
        # regular expression bases parser
        for link, text in re.findall(r'''href=[ "']([^ "']+)[ "']>([^<]+)''', data, re.DOTALL):
            print repr((text, link))
            for searchterm in linkterms:
                if text.lower().find(searchterm) > -1:
                    print searchterm,
                    print repr((text, link))
                    if link.startswith('http://'):
                        ret.append(link)
                    else:
                        ret.append(urlparse.urljoin(url, link))
                    break # break out of inner loop
    return ret


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


def spider(seeds):
    def ALRMhandler(signum, frame):
        print 'Signal handler called with signal', signum
    
    def INFOhandler(signum, frame):
        print "current frontier: %d, new frontier %d, dupes %d, current depth: %d" % (len(frontier), len(newfrontier), len(dupelist), page['level'])
        delta = time.time() - STARTTIME
        print "%d urls in %d s, %.2f urls/s" % (urlcount, delta, urlcount/delta)
    
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
        while frontier:
            page = frontier.pop()
            links = extract_links(page['url'], page['ref'])
            dupelist.add(page['url'])
            for link in links:
                if link not in dupelist and page['level'] < MAXLEVEL:
                    newfrontier.append(dict(url=str(link), ref=page['url'], level=page['level']+1))
                    dupelist.add(link)
        print len(newfrontier)
        frontier = newfrontier[:]
        print len(frontier)
    

print 'ARCiving to %r' % ('spider-hudora-%s.arc.bz2' % time.strftime('%Y%m%d%H%M'))
arc = ARCive.ARCive('spider-hudora-%s.arc.bz2' % time.strftime('%Y%m%d%H%M'), 'w')

starturls = [
'http://babybutt.erwinmueller.de/eshop/index.php?db_sess=fa516d7246872e3c8e785402253ee51a&dbsid=11&ss_shop=bb&',
'http://clusty.com/search?input-form=clusty-simple&v%3Asources=http://www.sportscheck.com/is-bin/INTERSHOP.enfinity/WFS/Sportscheck-SportscheckDe-Site/de_DE/-/EUR/SPM_BrowseCatalog-Start;sid=_PHZNufT-andNqEyfHHE9LKDsZ3e4tpMMVFC3iHH5VyeqkU8eXGtKZBqqnx8Tw==?CategoryName=sh13113514&Pfad=line&query=hudora',
'http://de.altavista.com/web/results?itag=ody&q=hudora&kgs=1&kls=0',
'http://de.search.yahoo.com/search?p=hudora&fr=yfp-t-501&ei=UTF-8&meta=vl%3D',
'http://de.vivisimo.com/search?input-form=simple-vivisimo-com&query=hudora&v%3Aproject=de-vivisimo-com&v%3Asources=Web&dlang=de&language=all&x=0&y=0',
'http://de.vivisimo.com/search?input-form=simple-vivisimo-com&query=hudora&v%3Aproject=de-vivisimo-com&v%3Asources=Web&dlang=de&language=german&x=0&y=0',
'http://del.icio.us/search/?fr=del_icio_us&p=hudora&type=all',
'http://en.wikipedia.org/wiki/Special:Search?search=hudora&go=Go',
'http://meta.rrzn.uni-hannover.de/meta/cgi-bin/meta.ger1?start=1&eingabe=hudora&mm=and&maxtreffer=200&time=3&hitsPerServer=2&textmenge=2&wissRank=on&sprueche=on&QuickTips=beschleuniger&linkTest=no&check_time=3&dmoz=on&exalead=on&suchclip=on&wiki=on&harvest=on&witch=on&overture=on&fastbot=on&fportal=on&Nachrichten=on&Usenet=on&firstsfind=on&cpase=on&metarss=on&neomo=on&nebel=on&audioclipping=on',
'http://msxml.excite.com/info.xcite/search/web/hudora',
'http://preis.info/index.aspx?such=hudora&image2.x=0&image2.y=0',
'http://preisvergleich.getprice.de/jsp/partner/getprice2005/search.jsp?name=hudora&Submit=suchen&navCategoryID=&priceRangeFrom=&priceRangeTo=',
'http://produktsuche.web.de/search.do?s=hudora',
'http://sads.myspace.com//Modules/Search/Pages/Search.aspx?fuseaction=advancedFind.results&searchtarget=tms&searchtype=myspace&t=tms&get=1&websearch=1&searchBoxID=Profile&searchString=hudora&q=hudora',
'http://search-desc.ebay.de/rollschuhe_W0QQfsooZ2QQfsopZ19QQftsZ2QQsalisZ77',
'http://search-desc.ebay.de/search/search.dll?sofocus=bs&sbrftog=1&from=R10&satitle=hudora&sacat=-1%26catref%3DC6&bs=Finden&fts=2&sargn=-1%26saslc%3D3&sadis=200&fpos=Postleitzahl&sabfmts=1&saobfmts=insif&ga10244=10425&ftrt=1&ftrv=1&saprclo=&saprchi=&salis=77&fhlc=1&fsop=1%26fsoo%3D1&coaction=compare&copagenum=1&coentrypage=search&fgtp=',
'http://search.abacho.com/de/abacho.de/index.cfm?q=hudora&country=de&x=0&y=0',
'http://search.ebay.de/search/search.dll?fsop=1&fsoo=1&from=R3&strKw=+&shortcut=4&siteid=77&satitle=hudora',
'http://search.lycos.com/?query=hudora&x=0&y=0',
'http://search.msn.com/results.aspx?q=hudora&FORM=MSNH',
'http://search.yahoo.com/search?ei=UTF-8&trackingType=go_search_home&p=hudora&fr=hsusgo1&sa.x=0&sa.y=0',
'http://search.yahoo.com/search?ei=UTF-8&trackingType=go_search_home&p=hudora&fr=hsusgo1',
'http://shopping.freenet.de/search.do?suggestItem=&searchFlags=0&categoryIdsSuggest=&userQuery=1&searchText=hudora&categoryId=&submit.x=0&submit.y=0',
'http://shopping.kelkoo.de/ctl/do/search?siteSearchQuery=hudora&fromform=true&x=0&y=0',
'http://shopping.yahoo.de/ctl/do/search?siteSearchQuery=hudora&fromform=true&x=0&y=0',
'http://suche.baur.de/servlet/weikatec.search.SearchServlet?ls=0&prodDetailUrl=http%3A%2F%2Fwww.baur.de%2Fis-bin%2FINTERSHOP.enfinity%2FWFS%2FBaur-BaurDe-Site%2Fde_DE%2F-%2FEUR%2FBV_DisplayProductInformation-ProductRef%3Bsid%3D8BABmNTUETIDmJI1jy4XWoGEvZygnH3hNmkoFkJ2pR8KfteTkhoVmhkWMDD7wg%3D%3D%3Fls%3D0%26ProductRef%3D%253CSKU%253E%2540Baur-BaurDe%26SearchBack%3D-1%26SearchDetail%3Dtrue&source=&resultsPerPage=99&searchandbrowse=&category2=&query=hudora&category=',
'http://suche.fireball.de/cgi-bin/pursuit?cat=fb_loc&x=0&y=0&query=hudora',
'http://suche.lycos.de/cgi-bin/pursuit?query=hudora&SITE=de&cat=loc',
'http://suche.web.de/search/dir/?mc=verzeichnis%40rubrik.eintrag%40home&su=hudora&smode=',
'http://suche.web.de/search/web/?mc=hp%40suche.suche%40home&su=hudora&su1=hudora&su2=',
'http://www.accoona.com/search?col=ac&expw=1&expb=0&expn=0&pg=1&order=0&qc=de&ql=de&qt=hudora#thebusiness',
'http://www.allesklar.de/s.php?words=hudora&location=&Submit=suchen',
'http://www.alltheweb.com/search?cat=web&cs=iso88591&q=hudora&rys=0&itag=crv&_sb_lang=pref',
'http://www.amazon.de/s/?url=index%3Daps&field-keywords=hudora&Go.x=0&Go.y=0&Go=Go',
'http://www.apollo7.de/a7db/index.php?query=hudora&template=E_RESULTS&ads=true&max_result=200&max_time=10000000&land=de%2Bcom&de_lycos=true&de_mirago=true&de_msn=true&de_sharelook=true&de_witch=true&de_yahoo=true&suchen=suchen',
'http://www.billiger.de/suche.html?searchstring=hudora&search=1&stat=1&implicit=1',
'http://www.bonprix.de/bp/search.htm?id=163980085878606507-0-46e17b22&nv=0%7C0%7C&qu=hudora',
'http://www.ciao.de/Hudora_Scooter_Big_Wheel__2433141',
'http://www.ciao.de/sr/q-hudora',
'http://www.dino-online.de/suchergebnis.html?query=hudora&submit.x=0&submit.y=0&fref=suche.dino-online.de&js=on',
'http://www.dooyoo.de/kinderzubehoere/_hudora/',
'http://www.erwinmueller.de/eshop/index.php?db_sess=1f3c454558b84272f1f6406d61d35579&dbsid=11&ss_shop=em&ss_a=em|suche||||||||||||hudora||&wmn=2003653akt=no',
'http://www.evendi.de/jsp/eVendi2004/search.jsp?name=hudora+&Submit=OK&navCategoryID=&priceRangeFrom=&priceRangeTo=',
'http://www.exalead.de/search/results?q=hudora&x=15&y=17&%24mode=allweb',
'http://www.excite.de/search/web/results/?q=hudora&l=',
'http://www.excite.de/search/web/results/?q=hudora&x=0&y=0&l=',
'http://www.excite.de/shopping/productresults/?from_search=1&query=hudora&cid=',
'http://www.flickr.com/search/?q=hudora&w=all',
'http://www.google.de/products?q=hudora&btnG=Produkte+suchen',
'http://www.google.de/search?hl=de&q=hudora&btnG=Google-Suche&meta=',
'http://www.heise.de/preisvergleich/?cat=spbadmin',
'http://www.heise.de/preisvergleich/?cat=spbasketball',
'http://www.heise.de/preisvergleich/?cat=spboxen',
'http://www.heise.de/preisvergleich/?cat=spcrosst',
'http://www.heise.de/preisvergleich/?cat=spfittsonst',
'http://www.heise.de/preisvergleich/?cat=spfootball',
'http://www.heise.de/preisvergleich/?cat=spfussball',
'http://www.heise.de/preisvergleich/?cat=spgym',
'http://www.heise.de/preisvergleich/?cat=sphandball',
'http://www.heise.de/preisvergleich/?cat=sphantelbank',
'http://www.heise.de/preisvergleich/?cat=sphanteln',
'http://www.heise.de/preisvergleich/?cat=sphomet',
'http://www.heise.de/preisvergleich/?cat=spkleintrain',
'http://www.heise.de/preisvergleich/?cat=spkraft',
'http://www.heise.de/preisvergleich/?cat=splaufbae',
'http://www.heise.de/preisvergleich/?cat=spoutfbfan',
'http://www.heise.de/preisvergleich/?cat=spoutfbschuhe',
'http://www.heise.de/preisvergleich/?cat=spoutprotek',
'http://www.heise.de/preisvergleich/?cat=spoutskate',
'http://www.heise.de/preisvergleich/?cat=spouttorwart',
'http://www.heise.de/preisvergleich/?cat=spradkinder',
'http://www.heise.de/preisvergleich/?cat=spruder',
'http://www.heise.de/preisvergleich/?cat=spsquash',
'http://www.heise.de/preisvergleich/?cat=spstepper',
'http://www.heise.de/preisvergleich/?cat=sptennis',
'http://www.heise.de/preisvergleich/?cat=sptennissaiten',
'http://www.heise.de/preisvergleich/?cat=sptischtennis',
'http://www.heise.de/preisvergleich/?cat=spvolleyball',
'http://www.heise.de/preisvergleich/?fs=hudora&x=0&y=0&in=',
'http://www.heise.de/preisvergleich/?o=82',
'http://www.heise.de/preisvergleich/?o=83',
'http://www.heise.de/preisvergleich/?o=87',
'http://www.hotbot.com/?query=hudora&ps=&loc=searchbox&tab=web&mode=search&currProv=ask',
'http://www.idealo.de/preisvergleich/MainSearchProductCategory.html',
'http://www.jako-o.de/produkt/de/produkt_detail.mb1?mb_f020_id=WHxE-mPC0-kQzasjajz8&fag=d&lang=de&set=suche&subset=suche&suchtext=hudora&detail=on&p_id=5017283&mb_v301_g=1&wmnr_show=92&mb_v301_ch=43737',
'http://www.jako-o.de/produkt/de/produkt_detail.mb1?mb_f020_id=Z7XIR8k6Y-EQzasjszz8&fag=d&lang=de&set=suche&subset=suche&suchtext=hudora&detail=on&p_id=5017283&mb_v301_g=1&wmnr_show=92&mb_v301_ch=74845',
'http://www.kanoodle.com/results.html?query=hudora&x=0&y=0',
'http://www.kidoh.de/suche.php?PUBLICAID=7c9610797ac2e411222cc2450de697c2&start=0&mode=suche&suche=hudora&x=0&y=0',
'http://www.mamma.com/Mamma?utfout=1&qtype=0&query=hudora&Submit=  Search  ',
'http://www.metacrawler.com/info.metac/search/web/hudora/1/-/1/-/-/-/1/-/-/-/1/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/417/top/-/-/-/1',
'http://www.mister-wong.com/search/?search_type=w&keywords=hudora&btn=search',
'http://www.mistershoplister.de/hudora',
'http://www.mytoys.de/is-bin/INTERSHOP.enfinity/eCS/Store/de/-/DEU/Mt_BrowseCatalog-N;sid=sq5c9rxWmrNe9vq3MtU8_r1cO32-UsiqyLk=?CategoryName=de_DE-so%2eka%2e15%2e40&pg=0&sz=16&lnav=sport/inc/sport_navi_left&bnr=232_so_outdoor.jpg&ziel=sportnavi&mc=ove_095',
'http://www.mytoys.de/is-bin/INTERSHOP.enfinity/eCS/Store/de/-/DEU/Mt_DisplaySearchResult-Start;sid=2MQSlDiqwbIRlH521oJxnDmgyoH4USDlFB0=?key=hudora&cat=de_DE&sort=sd&pg=0',
'http://www.mytoys.de/is-bin/INTERSHOP.enfinity/eCS/Store/de/-/DEU/Mt_DisplaySearchResult-Start;sid=sq5c9rxWmrNe9vq3MtU8_r1cO32-UsiqyLk=?key=hudora&cat=de_DE&sort=sd&pg=0',
'http://www.neckermann.de/index.mb1?mb_f020_id=zl7HChS_xjfIJ9gnnUk1X0DjzDsHDsW9&vkh=0461&linktracking_nr=BUo96xmJvGWLXM7vhhiXX-WjazPLaW8&tgs_group=&ct=1&mb_v301_ch=ab2ea',
'http://www.otto.de/is-bin/INTERSHOP.enfinity/WFS/Otto-OttoDe-Site/de_DE/-/EUR/OV_ViewFHSearch-Search;sid=Rkrckgssg0eUk03wQuT8UF58jGc6Kb-ez6a6CvqGFFV53Fkz4wR3_gb05L1l-Q==?ls=0&commit=true&fh_search=hudora&fh_search_initial=hudora&stype=N',
'http://www.otto.de/is-bin/INTERSHOP.enfinity/WFS/Otto-OttoDe-Site/de_DE/-/EUR/OV_ViewFHSearch-Search;sid=xj6UoeETQG8RoafyRkS9gfq_DBNyGlWhT9IR-3JilCEx77MMY3A_zezLtysjww==?ls=0&commit=true&fh_search=hudora&fh_search_initial=hudora&stype=N',
'http://www.paperazzi.de/cgi-bin/pap_engine_v8.pl?suche=hudora&image.x=0&image.y=0',
'http://www.paperball.de/index.html?send=true&query=hudora&x=0&y=0&cat=loc',
'http://www.preis.de/index.htm',
'http://www.preisroboter.de/ergebnis102830.html',
'http://www.preissuchmaschine.de/psm_frontend/main.asp?kid=3-563-3342',
'http://www.preissuchmaschine.de/psm_frontend/main.asp?suche=hudora',
'http://www.preistrend.de/suchen.php?q=hudora&s=0&a=&z=&x=0&y=0',
'http://www.quelle.de/is-bin/INTERSHOP.enfinity/WFS/Quelle-quelle_de-Site/de_DE/-/EUR/Q_FreeSearch-Start;sid=FoQD8ABd2egO8Ea8lv2BphTxbZruGzuZrOl47u22?search_input=hudora&search_free=hudora&fh_view_size=10&fh_sort_by=&enfaction=msearch&action=search&Linktype=E&fh_location=%2F%2Fquelle_de%2Fde_DE',
'http://www.rollsport.de/',
'http://www.rollsport.de/advanced_search_result.php?keywords=hudora&osCsid=1fdd16378f3e607dd03a4476bb8b9f2e&x=0&y=0',
'http://www.sharelook.de/sldb/SLDB_db.php?keyword=hudora&suche_starten=suchen&seite=400001&template=template_suchen&next_results=0&ad=1',
'http://www.shopping-profis.de/preisvergleich/suche-n1.html?q=hudora&mc=&x=0&y=0',
'http://www.spock.com/q/dornseif',
'http://www.sportscheck.com/is-bin/INTERSHOP.enfinity/WFS/Sportscheck-SportscheckDe-Site/de_DE/-/EUR/SPM_ParametricSearch-Progress;sid=_PHZNufT-andNqEyfHHE9LKDsZ3e4tpMMVFC3iHH5VyeqkU8eXGtKZBqqnx8Tw==',
'http://www.supabillig.com/a/result.jsp?cr=f&query=Hudora',
'http://www.tchibo.de/is-bin/INTERSHOP.enfinity/eCS/Store/de/-/EUR/TdTchParametricSearch-Start?search_query_keyword=hudora',
'http://www.topxplorer.de/cgi-bin/search.cgi?query=hudora&where=de',
'http://www.topxplorer.de/cgi-bin/search.cgi?query=hudora&where=web',
'http://www.web-archiv.de/index.php?qry=hudora&cms=suche_internet&imageField.x=0&imageField.y=0',
'http://www.webcrawler.com/webcrawler/ws/results/Web/hudora/1/417/TopNavigation/Relevance/zoom=off/_iceUrlFlag=7?_IceUrl=true',
'http://www.wisenut.com/search/query.dll?q=hudora',
'http://www.witch.de/search-result.php?cn=0&search=hudora',
'http://www.xing.com/app/search?op=universal&universal=hudora',
'http://www.yatego.com/index.htm?&cl=mallsearch&tab=shopping&std=1&startCat=&query=hudora&catonly=false&x=0&y=0',
'http://www.yopi.de/index.php?template=search_result&search_mode=basic&search_string=hudora&cat_id=0',
'http://www.yopi.de/index.php?template=search_result&w=hudora&l=a&search_mode=category&cat_id=343',
'http://www.yopi.de/index.php?template=search_result&w=hudora&l=a&search_mode=category&cat_id=516',
'http://www.yopi.de/index.php?template=search_result&w=hudora&l=a&search_mode=category&cat_id=744',
'http://search.dooyoo.de/search/both/hudora/0/?suche=hudora',
'http://www.alexa.com/data/details/traffic_details?url=http%3A%2F%2Fwww.hudora.de%2F',
'http://www.alexa.com/data/details/related_links?url=hudora.de',
'http://www.alexa.com/data/details/traffic_details?url=hudora.de',
'http://searchdns.netcraft.com/?host=hudora.de&position=limited&lookup=Wait..',
'http://toolbar.netcraft.com/site_report?url=http://www.hudora.de',
'http://uptime.netcraft.com/up/graph?site=www.hudora.de',
'http://preis.info/Freizeit/k/Sport/fsosf.html',
'http://preis.info/Freizeit/k/Sport/fsosf/sonstiger_Sport/hsusk.html',
'http://preis.info/Freizeit/k/Sport/fsosf/Tischtennis/gsase.html',
'http://preis.info/Freizeit/k/Sport/fsosf/Nordic_Walking/oshsf.html',
'http://preis.info/Freizeit/k/Sport/fsosf/Hockey/hsgsh.html',
'http://preis.info/Freizeit/k/Sport/fsosf/Golf/gsask.html',
'http://preis.info/Freizeit/k/Sport/fsosf/Basketball/gsrst.html',
'http://preis.info/Freizeit/k/Sport/fsosf/Funsport/hsust.html',
'http://preis.info/Freizeit/k/Sport/fsosf/Volleyball/gsaso.html',
'http://preis.info/Freizeit/k/Sport/fsosf/Tennis/gsasu.html',
'http://preis.info/Freizeit/k/Sport/fsosf/Inline_Skates/rsrsust.html',
'http://preis.info/Freizeit/k/Sport/fsosf/Fussball/hsuse.html',
'http://preis.info/Freizeit/k/Wintersport/fstsa.html',
'http://preis.info/Freizeit/k/Spielwaren/fseso.html',
'http://preis.info/Freizeit/k/Schuhe/fsgst.html',
'http://preis.info/Freizeit/k/Fahrrad/fstsg.html',
'http://preis.info/Freizeit/k/Camping_Outdoor/tsasg.html',
]

random.shuffle(searchterms)
for searchterm in searchterms:
    urls = list(urls_for_searchengines(searchterm))[:5]
    random.shuffle(urls)
    starturls.extend(urls)
random.shuffle(searchterms)

foo = """californian-products.de
cphk.de
kettler.de
la-sports.de
panther-junior.com
puky.de
royalbeach.de
stamm-online.de
cratoni.com
fun4u-sports.de
fun4u-store.de
powerslide.de
vedes.de
hoffmann.de
tpactive.com
simbatoys.de
best-sport.com
happypeople.de
wehncke.de
hiskate.de
hudora.de
hyskate.de
royalbeach.com.hk
tunturi.com
kettlerusa.com
best-deutschland.de
KookaburraSpiel.com
accell-group.com
amco-sport.com
innnet.de
kettler-france.fr
kettler.at
kettler.co.uk
kettler.net
kettler.nl
pro.onet.pl
vaude.de
uhlsport.de
"""

spider(starturls)

if __name__  == '__main__S':
    def ALRMhandler(signum, frame):
        print 'Signal handler called with signal', signum
    signal.signal(signal.SIGALRM, ALRMhandler)

    
