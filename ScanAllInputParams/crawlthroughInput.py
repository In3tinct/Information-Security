import queue
from urllib.request import urlopen
from threading import Thread
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys

#Keeps a record of links which are already saved and are present just once in the queue
linksVisited=set()
linksWithInputParam=set()

def addLinksWithInputParam(link):
	if "?" in link:
		linksWithInputParam.add(link)
		print ("Printing URL with params")
		print (linksWithInputParam)

def do_stuff(q):
	while True:
		url = q.get()
		q.task_done()
		try:
			site=urlopen(url)
			siteContent=site.read()

			for links in BeautifulSoup(siteContent,'html.parser').find_all('a'):
				#Only proceed if links have href tag, many of the a tags
				#were having images and src in it
				#Ignoring if its an anchor tag having images inside				
				if len(links.find_all("img"))>0:
					#print ("Images")
					continue
				#all different file extensions could be replaced				
				if "pdf" in str(links):
					#print ("Escaping PDF")
					continue
				if links.has_attr('href'):
					linkUrl=links['href']
					#Checking for links which basically points to the same
		        	        #page using hash and doesn't starts with http
					##skipping the loop if not of same domain
					if linkUrl.count("#")>0:
						continue
					#For conditions where <a href='index.php?id=21'> and target is different from baseURL(Since no redirection is 						handled yet), Target Url=http://www.sallatykka.com/web/index.php, so have to map /web/ directory, so i do /../
					if not linkUrl.startswith('http') and "www" not in linkUrl:
						linkUrl=target+"/../"+linkUrl
						#print ("Incomplete: "+linkUrl)

					#skipping the loop if not of same domain
					if not linkUrl.startswith(baseURL):
						#print ("Escaping other domain")
						continue

	  				#Only letting visit the links which have not been
		                        #visited before
					if linkUrl not in linksVisited:
						linksVisited.add(linkUrl)
						q.put(linkUrl)		
						#print (linkUrl)
						addLinksWithInputParam(linkUrl)
			#print ("queue size before"+ str(q.qsize()))			
			#q.task_done()
			#print ("queue size after"+ str(q.qsize()))
							
		except:
			print ("An error occured while opening "+url)
			continue





#Expecting target as an argument, starting with http
#since href's start the link with http which we check for same domain above
if(len(sys.argv)<2):
	print ("Please pass a target url in the format http://www.example.com")
	exit(0)

target=sys.argv[1]

parsed=urlparse(target)

baseURL=parsed.scheme+"://"+parsed.netloc

print ("Target and BaseURL")
print (target)
print (baseURL)
q = queue.Queue()
q.put(target)

#Since we do not want to visit the root url again we put it into the visited list
#Also we may find a # in href which is a null value, but would revisit the same website
#Hence adding it too 
linksVisited.add(target)
linksVisited.add(target+'#')
linksVisited.add(baseURL)

num_threads = 10

for i in range(num_threads):
  worker = Thread(target=do_stuff, args=(q,))
  worker.setDaemon(True)
  worker.start()

#Since the threads were clearing the queues before new queue was added, the program was exiting, so running and infinite loop now
#q.join()

while True:
	continue
