from stravalib import Client

import requests as r
#import httplib

#from flask import Flask
#from flask import request



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
    
    def get_last_week(self,lim):
        for activity in self.client.get_activities(after="2016-08-01T00:00:00Z", limit=lim):
            print("{0.name} {0.moving_time}".format(activity))


sc=strava_class()
sc.login_vegard()
sc.get_last_week(10)
#sc.login_strava()
#sc.client


#athlete=client.get_athlete()




#url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri=MY_Url)

#print(url)


#req=r.get(MY_Url)


#url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri='https://www.strava.com/login')

#code = request.args.get(url)
#a=r.get(MY_Url)




