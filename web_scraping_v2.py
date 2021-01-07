# -*- coding: utf-8 -*-
"""
Stackoverflow link :
https://stackoverflow.com/questions/48665001/can-not-click-on-a-element-elementclickinterceptedexception-in-splinter-selen  
https://stackoverflow.com/questions/36026676/python-selenium-timeout-exception-catch   
  
https://wonderproxy.com/blog/a-step-by-step-guide-to-setting-up-a-proxy-in-selenium/   
https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905 
https://www.simplilearn.com/tutorials/selenium-tutorial/selenium-interview-questions-and-answers

Cookies-
https://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver

Free = proxy 

https://hidemy.name/en/proxy-list/?country=US&anon=1#list
    
Created on Mon Jan  4 09:25:21 2021

@author: phatn
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,TimeoutException,ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

def get_jobs(keyword,location, num_jobs, verbose,path,slp_time,proxy):   
    #Proxy and verbose are TRUE OR FALSE VALUES ONLY
      
    options = webdriver.ChromeOptions() # Picking the brower type
    options.headless = False #Make sure the browser doesnt show up, and its run in the background.....
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    if proxy:     
             PROXY = "172.96.172.68:3128" # IP:PORT or HOST:PORT  
             webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True #Getting chrome to accept the proxy
             options.add_argument('--proxy-server=%s' % PROXY)
     
            
    driver = webdriver.Chrome(executable_path=path, options=options) #Setting driver
    driver.set_window_size(1700, 1700) #Window size
    actions = ActionChains(driver) # Action movement
    url ='https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&sc.keyword=&locT=&locId=&jobType='                   
    driver.get(url) #Getting the URL
    jobs = []
    
    try:
        #Thanks stackoverflow       
        #Uses first variable in function to input job title
        search = driver.find_element_by_id("LocationSearch").clear()
        search = driver.find_element_by_id("KeywordSearch")
        search.send_keys(keyword)
        
        #Uses second variable in function to input Location.  Use 'City,State OR Region'
        search = driver.find_element_by_id("LocationSearch").clear()
        search = driver.find_element_by_id("LocationSearch")
        search.send_keys(location)
        search.send_keys(Keys.RETURN)
    except:
          print("Search Error")
           
    
    #Test for the "Sign Up" prompt and get rid of it.
    time.sleep(slp_time)
    
    #Using this so the program can ignore the exceptions
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,TimeoutException) 
    # Making sure that the filter only go off once
    count = 0 
    


    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
       
       
        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)
        

        #Test for the "Sign Up" prompt and get rid of it.
        
        
        try:
             selected= WebDriverWait(driver, slp_time).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "selected")))
             selected.click() 
             
             
        except (ElementClickInterceptedException,ElementNotInteractableException,StaleElementReferenceException):
            pass

        time.sleep(.1)

        try:
            driver.find_element_by_xpath('.//span[@alt="Close"]').click()
           
            #clicking to the X.
        except (NoSuchElementException,ElementNotInteractableException):
            pass
 
        
        if count < 2: 
            try:     
                
                clickable_filter1=WebDriverWait(driver, slp_time,ignored_exceptions=ignored_exceptions).until(
                EC.element_to_be_clickable((By.ID,"filter_minSalary")))
                driver.execute_script("arguments[0].click();", clickable_filter1)
                
               # WebDriverWait(driver, slp_time).until(
                #EC.presence_of_element_located((By.ID, "filter_minSalary"))).click()    
                
                
                clickable_filter2=WebDriverWait(driver, slp_time,ignored_exceptions=ignored_exceptions).until(
                EC.element_to_be_clickable((By.XPATH,'.//div[@class="checkboxBox"]')))
                driver.execute_script("arguments[0].click();", clickable_filter2)
                
               # WebDriverWait(driver, slp_time).until(
               # EC.presence_of_element_located((By.XPATH,'.//div[@class="checkboxBox"]'))).click()  
                
                clickable_filter3=WebDriverWait(driver, slp_time,ignored_exceptions=ignored_exceptions).until(
                EC.element_to_be_clickable((By.XPATH,'.//button[@class="applybutton gd-btn gd-btn-link gradient gd-btn-2 gd-btn-sm"]')))
                driver.execute_script("arguments[0].click();", clickable_filter3)
                
               # WebDriverWait(driver, slp_time).until(
               # EC.presence_of_element_located((By.XPATH, './/button[@class="applybutton gd-btn gd-btn-link gradient gd-btn-2 gd-btn-sm"]'))).click()  
                
                count = count + 1
                
                
                print('Salary filter is working', count)
            except TimeoutException:
                print('Can not find Salary filter')
                pass
            time.sleep(2)
            
        if count < 2: 
               try:
                   employess_filter1= WebDriverWait(driver, slp_time).until(
                   EC.presence_of_element_located((By.XPATH,'.//div[@class="filter more expandable"]')))
                   employess_filter1.click()
                   
                   employess_filter2 = WebDriverWait(driver, slp_time).until(
                   EC.presence_of_element_located((By.XPATH,'.//div[@class="filter more expandable expanded"]//div[@id="filter_employerSizes"]')))
                   employess_filter2.click()
                   
                   employess_filter3 = WebDriverWait(driver, slp_time).until(
                   EC.presence_of_element_located((By.XPATH,'//*[@id="dynamicFiltersContainer"]/div/div[1]/div[2]/div[2]/div[13]/ul/li[6]')))
                   #'.//ul[@class="css-1dv4b0s ew8xong0"]//li[@value="5"]')))
                   employess_filter3.click()
                   
                   time.sleep(1)   
                   
                   employess_filter4 = WebDriverWait(driver, slp_time).until(
                   EC.presence_of_element_located((By.XPATH,'.//div[@class="allDropdowns"]//div[@class="filter more expandable expanded applied"]')))
                   employess_filter4.click()
                  
                   count = count + 1 
                   
                   print('Company size filter working',count)
               except (NoSuchElementException,TimeoutException,StaleElementReferenceException,ElementNotInteractableException):               
                   print('Company filter failed')     

                   pass
       
        
    #   driver.refresh() #Bypassing the dom block on glassdoor
        #Going through each job in this page
    #   refresh_filter = WebDriverWait(driver, slp_time).until(           
    #    EC.presence_of_element_located((By.XPATH,'.//div[@class="allDropdowns"]//div[@class="filter more expandable expanded applied"]')))
    #    refresh_filter.click()
        
        
        try:
            job_buttons = driver.find_elements_by_class_name("jl") 
        except:
            break
        
        #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
        
            
     
            driver.execute_script("arguments[0].click();", job_button)
           
          
            #You might 
            time.sleep(1)
            collected_successfully = False
            Rating_collected_successfully =False
            
            while not collected_successfully:
              
                try:
                    company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                    company_name = -1
                
                try: 
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                    location = -1
                    
                
                try:  
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    #job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                     job_title = -1
                
                try: 
                    job_description = WebDriverWait(driver, slp_time).until(
                    EC.visibility_of_element_located((By.XPATH,'.//div[@class="jobDescriptionContent desc"]'))).text              
                    
                                       
                except (NoSuchElementException,TimeoutException,ElementNotInteractableException,StaleElementReferenceException):
                    job_description = -1
                    
                try:
                    salary_estimate = driver.find_element_by_xpath('.//span[@class="css-1uyte9r css-hca4ks e1wijj242"]').text
                    collected_successfully = True
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                    salary_estimate = -1 #You need to set a "not found value. It's important."    
                    
                #--------------------------------------------------------------------------------------------------------------  
                
            if verbose:
             print("Job Title: {}".format(job_title))
             print("Salary Estimate: {}".format(salary_estimate))
             print("Job Description: {}".format(job_description[:500]))             
             print("Company Name: {}".format(company_name))
             print("Location: {}".format(location))      
                
            while not Rating_collected_successfully:  
                 
                try:
                     culture_values = driver.find_element_by_xpath('.//strong[text()="Culture & Values"]//following-sibling::*').text
                   
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):                      
                       culture_values = -1
                try:
                       compensation_benefits = driver.find_element_by_xpath('.//strong[text()="Compensation & Benefits"]//following-sibling::*').text
                                       
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                      
                      compensation_benefits = -1
                try:
                    
                      career_opportunities = driver.find_element_by_xpath('.//strong[text()="Career Opportunities"]//following-sibling::*').text
                  
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                      
                       career_opportunities = -1
                      
                try:
                    work_life_balance = driver.find_element_by_xpath('.//strong[text()="Work/Life Balance"]//following-sibling::*').text
                 
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                    work_life_balance = 1
                        
                
                try:
                    rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
                    Rating_collected_successfully = True
                    
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                    
                    rating = -1 #You need to set a "not found value. It's important."
                    

            #Printing for debugging
            if verbose:
                print("Rating: {}".format(rating))   
                print("Compensation & Benefits: {}".format(compensation_benefits))
                print("Culture Values: {}".format(culture_values))
                print("Career Opportunities {}".format(career_opportunities))
                print("WorkLife Balance: {}".format(work_life_balance))


            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                tab_click=WebDriverWait(driver, slp_time,ignored_exceptions=ignored_exceptions).until(
                EC.element_to_be_clickable((By.XPATH,'.//span[text()="Company"]')))
                driver.execute_script("arguments[0].click();", tab_click)
                #driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()


                try:
                    size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                    size = -1

                try:
                    founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                    revenue = -1

              

            except (NoSuchElementException,TimeoutException,ElementClickInterceptedException,ElementNotInteractableException,StaleElementReferenceException):  
                #Rarely, some job postings do not have the "Company" tab.                
                    size = -1
                    founded = -1
                    type_of_ownership = -1
                    industry = -1
                    sector = -1
                    revenue = -1
                          
            if verbose: 
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
            
            
            try:
                rating_click=WebDriverWait(driver, slp_time).until(
                EC.presence_of_element_located((By.XPATH, './/span[text()="Rating"]')))
                driver.execute_script("arguments[0].click();", rating_click)
                
                try:
                        ceo = driver.find_element_by_xpath('.//*[@id="RatingContainer"]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]').text
                                       
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):                      
                        ceo = -1
                        
            except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException,TimeoutException):  
                #Rarely, some job postings do not have the "Company" tab.                
                    ceo = -1
            if verbose:
                print("Ceo: {}".format(ceo))

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Company Name" : company_name,
            "Location" : location,           
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "CEO" : ceo,
            "Overall Rating" : rating,
            "Compensation & Benefits" : compensation_benefits,
            "Career Opportunities" : career_opportunities,
            "Work Life Balance" : work_life_balance,
            "Culture Values" : culture_values,
  
            
            })
            #add job to jobs

        #Clicking on the "next page" button
        try:
            nextpages = WebDriverWait(driver, slp_time).until(
                EC.presence_of_element_located((By.XPATH, './/li[@class="next"]//a')))
            actions.move_to_element(nextpages).perform()
            nextpages.click()
            #driver.find_element_by_xpath('.//li[@class="next"]//a').click()
            #drop_box = WebDriverWait(driver, slp_time).until(
                   #EC.presence_of_element_located((By.XPATH,'.//div[@class="allDropdowns"]//div[@class="filter more expandable expanded applied"]')))
            #drop_box.click()
            
        except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break
            

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.