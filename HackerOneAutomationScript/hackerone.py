#!/usr/bin/env python3

import requests
import json
import threading
import Tkinter
import tkMessageBox
import webbrowser
import sys
import time
from datetime import datetime

#https://hackerone.com/directory?query=type%3Ahackerone&sort=published_at%3Adescending&page=1
#The above link was getting a json request for list of programs, I found it in the debug console in networks tab

userdata = { "brandDetails":[]}
oldList = []
intialized=0
count=0
	

def add_brand(brand):
  	userdata["brandDetails"].append(brand)

def filloldList():
	global oldList
	oldList = []
	for i in xrange(0,9):		
		oldList.append(userdata['brandDetails'][i]['name'])

def fetch():
	try:
		sys.stdout.flush();
		print "Starting:"
		print str(datetime.now())
		global intialized
		web=requests.get('https://hackerone.com/programs/search?query=type%3Ahackerone&sort=pblished_at%3Adescending&page=1')
		#json_data=web.json()
		json_data=json.loads(web.text)
	
		for i in xrange(0,9):
			
			brand = {}
    			brand["name"]=json_data['results'][i]['name']
    			#user["age"]=10
    			#user["country"]='USA'
    			add_brand(brand)
		#Making sure the old list is filled once, and updated only when a new program is added while comparing it with new list	
		if intialized==0:
			filloldList()
			intialized=intialized+1
			
		
		#TO TEST, UNCOMMMENT THE BELOW LINES
		#global count
		#if count==1:
		#	userdata['brandDetails'][4]['name']='ab'
		#count=count+1


		#Just checking with last ten programs	
		for i in xrange(0,9):
			if userdata['brandDetails'][i]['name'] in oldList:
				pass
		
			else:
				root = Tkinter.Tk()
				root.withdraw()
				message=", Just Got added in the list"
				message1="Happy Hacking"
				root.option_add('*Dialog.msg.width', 50)
				tkMessageBox.showinfo(userdata['brandDetails'][i]['name']+message, message1)
				root.update()
				print userdata['brandDetails'][i]['name']
				filloldList()
				webbrowser.open('https://hackerone.com/directory?query=type%3Ahackerone&sort=published_at%3Adescending&page=1')
				break;
		print "Executed"
	except requests.ConnectionError:
		print "Error while making a get request, Will retry again in specified time"							

if __name__ == "__main__":
	while True:
		fetch()
		#Running after every 5 minutes
		time.sleep(300)
		
	#print userdata
	
