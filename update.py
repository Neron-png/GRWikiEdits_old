import requests
import json
import re
from datetime import date
import time



todaylist = []
strToday = date.today()
# format of date : 2020-11-20
d8 = strToday.strftime("%Y-%m-%d")
#d8 = today's date



#get last RevID
with open('last_revid.txt', 'r') as lastrev_stored:
    lastrev = lastrev_stored.read()
    lastrev = int(lastrev)
    lastrev_stored.close()


#Turn IP list file into list
with open("userlist.txt", "r") as usrList:
    userlist = usrList.readlines()
    userlist = [x.replace('\n', '') for x in userlist]
    usrList.close()


def updateLastRev(revid):
    with open('last_revid.txt', 'w') as lastrev_stored:
        lastrev = int(lastrev_stored.write(revid))
        lastrev_stored.close()


def check(IP):
    global DATA
    global lastrev
    API = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "usercontribs",
        "ucuser": IP
    }


    R = requests.get(url=API, params=PARAMS)
    DATA = R.json

    #Turns response json into string
    DATA = json.dumps(DATA(), sort_keys=True, indent=4)
    #print (DATA)

    #Tests to see if IP has made any edits in wikipedia
    if int(getRev()) > int(lastrev):
        print ("Success for "+ IP)
        updateLastRev(getRev())
        lastrev = getRev()
        check_result = True

    else:
        print ("Nothing today from "+ IP)
        check_result = False

    return check_result

#Get's the revision id to generate link
def getRev():
    revid = re.search('(?<="revid": )(.*)(?=,)', DATA).group()
    return revid

def getArt():
    art = re.search('(?<="title": ")(.*)(?=",)', DATA).group()
    return art




while True:
    #Goes through the list of identified IP's and test to see if any has made changes today
    for i in range(len(userlist)):

        IP = userlist[i]
        updated = check(IP)

    ######## TO BE REPLACED WITH TWITTER UPLOAD LINK
        if updated:
            revid = getRev()
            article = getArt()
            wikiURL = "https://en.wikipedia.org/w/index.php?diff=" + revid
            print (wikiURL)
            todaylist.append("Το άρθρο \"" + article + "\" υπέστη επεξεργασία από ανώνυμο άτομο της Βουλής. " + wikiURL)


    #Writes successful links's to file
    with open('today_links.txt', 'w') as filehandle:
        for listitem in todaylist:
            filehandle.write('%s\n' % listitem)


    ######## TO BE REPLACED WITH TWITTER UPLOAD LINK
    time.sleep(6)
