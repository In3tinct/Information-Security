import urllib2
from bs4 import BeautifulSoup
import threading
import Queue
import sys
import time
import signal

#Keeps a record of links which are already saved and are present just once in the queue
linksVisited=set()

class workerThreads(threading.Thread):
	def __init__(self,queue):
		threading.Thread.__init__(self)
		self.queue=queue

	def run(self):
	  while True:
	  	url=self.queue.get()
	    	try:
			site=urllib2.urlopen(url)
			siteContent=site.read() 

			for links in BeautifulSoup(siteContent).find_all('a'):
				#Only proceed if links have href tag, many of the a tags
				#were having images and src in it
				if links.has_attr('href'):
					linkUrl=links['href']

					#Checking for links which basically points to the same
		        	        #page using hash and doesn't starts with http
					if not linkUrl.startswith('http://'):
						linkUrl=target+linkUrl
						#print "This is it%s"%linkUrl
				
					#skipping the loop if not of same domain
					if not linkUrl.startswith(target):
						continue 

	  				#Only letting visit the links which have not been
		                        #visited before
					if linkUrl not in linksVisited:
						linksVisited.add(linkUrl)
						self.queue.put(linkUrl)		
						print linkUrl
	 	
		except urllib2.HTTPError as e:
			#if e.code==404:
			#print "Page not found"
			continue
		except:
			#print "An error occured while opening "+url
			continue
#Initiating a queue
queue=Queue.Queue()

#Expecting target as an argument, starting with http and ending with a /
#since href's start the link with http which we check for same domain above
if(len(sys.argv)<2):
	print "Please pass a target url in the format http://www.example.com"
	exit(0)

target=sys.argv[1]

#Since we do not want to visit the root url again we put it into the visited list
#Also we may find a # in href which is a null value, but would revisit the same website
#Hence adding it too 
linksVisited.add(target)
linksVisited.add(target+'#')

allThreads=[]
for i in range(10):

	threadInstance=workerThreads(queue)
	threadInstance.setDaemon('True')
	threadInstance.start()
	allThreads.append(threadInstance)

queue.put(target)

for j in allThreads:
	j.join()

queue.join()

#while True:
#	if queue.empty():
#		time.sleep(5)
#		break
print "Crawling completed"		
