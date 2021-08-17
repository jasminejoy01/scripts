"""
Date: Aug  4 23:02:44 2018
Jasmine Joy

Login Automation using Selenium
"""

import shutil, datetime, os, time
from selenium import webdriver

def pushNotification():
    filename ='C:/Users/jjoy/Desktop/pushNotification.xlsm'
    os.startfile(filename)

def site_login():
    driver.get ('https://WebsiteURL')
    driver.find_element_by_id("loginbtn").click() #Login Button
    usernameStr = 'username'
    passwordStr = 'password'  
    driver.find_element_by_id("login").send_keys(usernameStr)
    driver.find_element_by_id ("password").send_keys(passwordStr)
    driver.find_element_by_id("login-submit").click()

try:
	#Accessing existing Chrome Driver
    driver = webdriver.Chrome(executable_path="C:/chromedriver_win32/chromedriver.exe")
    site_login()
    driver.find_element_by_id("loginbtn").click()
    
	#Handle Pop-ups
    try:
        driver.find_element_by_class_name('popup-close')
        driver.find_element_by_class_name("popup-close").click()
    except:
        print "Pop-Up skipped"
    
	##Finding Export Button
    driver.find_element_by_id("exportbutton").click()
    
	##Push Email notification
    pushNotification() 
    
    #Close Browser
    driver.quit()
	
except Exception as inst:
    print inst, "Repair: Check Latest Chrome Browser Update date and install new version of Chrome Driver"
    filename ='C:/Users/jjoy/Desktop/PushFailUpdate.xlsm'
    os.startfile(filename)

    

