# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 17:52:01 2021

@author: phatn
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def get_jobs2(keyword, num_jobs, verbose,path,slp_time):   
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1520, 1500) 
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=S&locId=3426&jobType="
     
    
  
    driver.get(url)
    jobs = []
    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
       closed=False
       #Let the page load. Change this number based on your internet speed.
       #Or, wait until the webpage is loaded, instead of hardcoding it.
       time.sleep(slp_time)
   
       #Test for the "Sign Up" prompt and get rid of it.
       
       try:
           driver.find_element_by_class_name("selected").click()
       except ElementClickInterceptedException:
           pass

       time.sleep(.1)
       try:
            driver.find_element_by_css_selector('[alt="Close"]').click()
            clickable = False
            employess = False
            
            print('Pop-up has been closed')
       except NoSuchElementException:
            print('There no such element for pop-up')
            pass
        #Filter by company with salary
       while not clickable: 
            try:                
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "filter_minSalary"))).click()    
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'.//div[@class="checkboxBox"]'))).click()  
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, './/button[@class="applybutton gd-btn gd-btn-link gradient gd-btn-2 gd-btn-sm"]'))).click()  
                clickable = True 
                print('Salary filter is working')
            except NoSuchElementException:
                print('Can not find Salary filter')
                pass
            time.sleep(.1)
            #Filtering by big companys 
            while not employess: 
                try:
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,'.//div[@class="filter more expandable"]'))).click() 
                    
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,'.//div[@class="filter more expandable expanded"]//div[@id="filter_employerSizes"]'))).click() 
                    
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,'.//ul[@class="css-1dv4b0s ew8xong0"]//li[@value="5"]'))).click() 
                    
                    time.sleep(.05)   
                    
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,'.//div[@class="allDropdowns"]//div[@class="filter more expandable expanded applied"]'))).click() 
                   
                    employess = True 
                    print('Company size filter working')
                except NoSuchElementException:               
                    print('Company filter failed')     
                    
                    pass
            #going tho all the jobs    
            job_buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'jl')))
        
           # driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
           
            for job_button in job_buttons:  
    
                print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
                if len(jobs) >= num_jobs:
                    break
    
                job_button.click()  #You might 
                time.sleep(2)
                collected_successfully = False
                
                while not collected_successfully:
                    try:
                        company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                        location = driver.find_element_by_xpath('.//div[@class="location"]').text
                        job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                        job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                        collected_successfully = True
                    except :
                        time.sleep(5)
            