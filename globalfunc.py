import sys
import platform
import localconfig
if platform.system() == "Windows":
        sys.path.append(localconfig.winpath)
else:sys.path.append(localconfig.linuxpath)
import pywikibot
from pywikibot.data import api

useWiki= pywikibot.Site('en','wikipedia')

def callAPI(params):
    req = api.Request(useWiki, **params)
    return req.submit()
def getUserList():
        site = pywikibot.getSite()
        params = {'action': 'query',
            'list': 'allusers',
            'augroup': 'ipblock-exempt',
            'aulimit':'5000',
            'format':'json'}
        result = callAPI(params)
        reg = result["query"]["allusers"]
        userlist=""
        detaillist=""
        for user in reg:
                username = user["name"]
                userlist = userlist+ "\n"+"*{{User|"+user["name"]+"}}"
                try:detaillist = detaillist + "\n*" + query(username)
                except:
                        print "FAILED - " + username
        sendPage(userlist, "raw")
        sendPage(detaillist, "list")
        return
def query(user):
        letitle = "User:" + user
        #letitle = letitle.split("&quot;")[0]
        site = pywikibot.getSite()
        params = {'action': 'query',
         'list': 'logevents',
         'letype': 'rights',
         'letitle':letitle,
         'format':'json',
	 'lelimit':'100'
              }
        #print 'LETITLE: ' +letitle
        result = callAPI(params)
        log = result["query"]["logevents"]
        #print log
        for event in log:
                if event["params"]["oldgroups"] == '': event["params"]["oldgroups"]="None"
                if not "ipblock-exempt" in event["params"]["oldgroups"] and "ipblock-exempt" in event["params"]["newgroups"]:return event["timestamp"]+ " [[User:" + event["user"] + "|" + event["user"] + "]] ([[User talk:" + event["user"] + "|talk]] | [[Special:Contributions/" + event["user"] + "|contribs]] | [[Special:Block/" + event["user"] + "|block]])" + " changed rights for [[" +event["title"] + "]] from " + ','.join(event["params"]["oldgroups"]) + " to " + ','.join(event["params"]["newgroups"]) + " per '" + event["comment"] + "'"
                #print "Event: "+event["timestamp"]+ " " + event["user"] + " changed userrights for " +event["title"] + " from " + event["rights"]["old"] + " to " + event["rights"]["new"] + " because " + event["comment"]
def sendPage(text, txtformat):
    #print text
    summary = localconfig.summary
    if txtformat == "list":
        site = pywikibot.getSite()
        pagename = localconfig.listlocation
        page = pywikibot.Page(site, pagename)
        #print text
        pagetxt = page.get()
        page.put(text, comment=summary)
    elif txtformat == "raw":
        site = pywikibot.getSite()
        pagename = localconfig.rawlocation
        page = pywikibot.Page(site, pagename)
        pagetxt = page.get()
        page.put(text, comment=summary)
def startAllowed():
        site = pywikibot.getSite()
        pagename = localconfig.gopage
        page = pywikibot.Page(site, pagename)
        start = page.get()
        if start == "Run":
                return True
        else:
                return False
