import requests
import json

userlist = []


def check(IP):
    
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
    if DATA.find("comment") > 0:
        userlist.append(IP)
        check_result = ("Success for", IP)
    else:
        check_result = ("Nothing from ", IP)
    
    return check_result




#Loops through a loop of Greek Parliament's IP addresses
for i in range(0,256): #set to 256 for full list
    IP = "195.251.32.%i" %(i)
    print (check(IP))
    #195.251.32.51
    #195.251.32.62

#Writes successful IP's to file    
with open('userlist.txt', 'w') as filehandle:
    for listitem in userlist:
        filehandle.write('%s\n' % listitem)
print ("Found the following IP's")
print (userlist)
    
    