from stravalib import Client

import requests as r
from datetime import datetime, timedelta
import re
#import httplib

#from flask import Flask
#from flask import request

d=datetime.today()


class strava_activity(object):
    def __init__(self,name):
        self.name=name                  #str of name
        self.distance=0                 #m
        self.time=timedelta(seconds=0)  #HH:MM:SS
        self.kudos=0                    #nr

class strava_class(object):
    def __init__(self):
        self.client = Client()



    def login_vegard(self):
        MY_STRAVA_CLIENT_ID=14139
        MY_STRAVA_CLIENT_SECRET='d753993b6646b15440914a6477e0d0e594b6a5b5'
        code='3436d2f7d6b3926667097f39cb9d07eeb8fdc9d2'
        access_token = self.client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID,client_secret=MY_STRAVA_CLIENT_SECRET,code=code)
        self.client.access_token=access_token

    def login_other():
        MY_Url='http://127.0.0.1:5000'
        url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri=self.MY_Url)
        #Start web server
        #Get the user to click the link
        #read out the code from web server
        #stop web server
        return 0
    
    def get_last_days(self,days,lim):
        week_ago=datetime.today()-timedelta(days=days)
        week_ago_s=week_ago.strftime("%Y-%m-%dT%H:%M:%S:00Z")

        act=[]              #Class to store the activitys
        
        types=['name','distance','moving_time','kudos_count']
        #streams=self.client.get_activity_streams()
        len=0
        for ac in self.client.get_activities(after=week_ago_s, limit=lim):
            #print("{0.name} {0.distance} {0.moving_time} {0.kudos_count}".format(ac))
            act.append(strava_activity(name="{0.name}".format(ac)))
            
            act[-1].distance=float((re.findall("\d+\.\d+","{0.distance}".format(ac)))[-1])

            t = datetime.strptime("{0.moving_time}".format(ac),"%H:%M:%S")
            act[-1].time=timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            
            act[-1].kudos=int("{0.kudos_count}".format(ac))       

        return act
    
#datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
#datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S:00Z")


sc=strava_class()
sc.login_vegard()
aa=sc.get_last_days(30,10)

#Count kudos last mnth:
tkudos=0
tdistance=0
ttime=timedelta(seconds=0)

for ac in aa:
    tkudos=tkudos+ac.kudos
    tdistance=tdistance+ac.distance
    ttime=ttime+ac.time

print("Antal treningsøkter de siste 30 dagene:" + repr(len(aa)))
print("Antall km de siste 30 dagene:" + repr(tdistance/1000))
print("Antall kudos siste 30 dagene:" + repr(tkudos))
print("Total treningstid de siste 30 dagene:" + str(ttime))


#for acc in aa:
#    print(acc('name'))

#sc.login_strava()
#sc.client


#athlete=client.get_athlete()

#url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri=MY_Url)

#print(url)


#req=r.get(MY_Url)


#url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri='https://www.strava.com/login')

#code = request.args.get(url)
#a=r.get(MY_Url)



