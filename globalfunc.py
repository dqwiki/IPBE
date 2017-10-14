import sys
import platform
import localconfig
if platform.system() == "Windows":
        sys.path.append(localconfig.winpath)
else:sys.path.append(localconfig.linuxpath)
import pywikibot
import datetime
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
                detaillist = detaillist + "\n*" + query(username)
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
                skipold = False
                skipnew = False
                if event["params"]["oldmetadata"] == []:
                        event["params"]["oldmetadata"]="None"
                        skipold = True
                if event["params"]["newmetadata"] == []:
                        event["params"]["newmetadata"]="None"
                        skipnew = True
		for line in event["params"]["oldmetadata"]:
                        if skipold:
                                old=False
                                continue
			if line["group"] =="ipblock-exempt":
				old=True
				continue
			else:old=False
		for line in event["params"]["newmetadata"]:
                        if skipnew:
                                new=False
                                continue
			if line["group"] =="ipblock-exempt":
				new=True
				continue
			else:new=False
		if not old and new:
			sendToTalk(event["timestamp"],event["title"],event["comment"],event["user"])
			oldgroups = ""
			newgroups = ""
			count=0
			for entry in event["params"]["oldmetadata"]:
				if count == 0:
					oldgroups += entry["group"]
					count+=1
				else:
					oldgroups += ", "+entry["group"]
					count+=1
			count=0
			for entry in event["params"]["newmetadata"]:
				if count == 0:
					newgroups += entry["group"]
					count+=1
				else:
					newgroups += ", "+entry["group"]
					count+=1
			return event["timestamp"]+ " [[User:" + event["user"] + "|" + event["user"] + "]] ([[User talk:" + event["user"] + "|talk]] | [[Special:Contributions/" + event["user"] + "|contribs]] | [[Special:Block/" + event["user"] + "|block]])" + " changed rights for [[" +event["title"] + "]] from " + oldgroups + " to " + newgroups + " per '" + event["comment"] + "'"
		#print "Event: "+event["timestamp"]+ " " + event["user"] + " changed userrights for " +event["title"] + " from " + event["rights"]["old"] + " to " + event["rights"]["new"] + " because " + event["comment"]
def sendToTalk(timestamp,username,reason,admin):
	username = username.split("User:")[1]
	pagename = localconfig.talklocation
        page = pywikibot.Page(useWiki, pagename)
        pagetxt = page.get()
	now = datetime.datetime.now()
	dateofchange = timestamp.split("Z")[0]
	year = dateofchange.split("-")[0]
	try:
		if username in pagetxt.split("=="+year+"==")[1]:return
	except:
		if username in pagetxt.split("== "+year+" ==")[1]:return
	if year != str(now.year):return
	if now.month > 9:
                month = dateofchange.split("-")[1]
	else:
                month = dateofchange.split("-")[1].replace("0","")
	monthword = now.strftime("%B")
	if not "=="+year+"==" in pagetxt and not "== "+year+" ==" in pagetxt:
		pagetxt += "\n=="+year+"==\n"
	try:pageyear = pagetxt.split("=="+year+"==")[1]
	except:pageyear = pagetxt.split("== "+year+" ==")[1]
	if not monthword in pageyear:
		pagetxt += "\n==="+monthword+"===\n"
	if month == str(now.month):
		pagetxt += "\n*{{UserIPBE|" + username+"}} - Granted by "+admin+" - "+reason+" ~~~~"
	else:return
	summary = localconfig.summary
        page.put(pagetxt, comment=summary + " - Adding [[User:"+username+"|"+username+"]]")
				
def sendPage(text, txtformat):
    #print text
    summary = localconfig.summary
    if txtformat == "list":
        site = pywikibot.getSite()
        pagename = localconfig.listlocation
        page = pywikibot.Page(useWiki, pagename)
        #print text
        pagetxt = page.get()
        page.put(text, comment=summary)
    elif txtformat == "raw":
        site = pywikibot.getSite()
        pagename = localconfig.rawlocation
        page = pywikibot.Page(useWiki, pagename)
        pagetxt = page.get()
        page.put(text, comment=summary)
def startAllowed():
        site = pywikibot.getSite()
        pagename = localconfig.gopage
        page = pywikibot.Page(useWiki, pagename)
        start = page.get()
        if start == "Run":
                return True
        else:
                return False
