# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:25:21 2021

@author: phatn
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,TimeoutException,ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def get_jobs2(keyword, num_jobs, verbose,path,slp_time):   
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1700, 1700) 
    actions = ActionChains(driver)
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=S&locId=3426&jobType="
    clickable= False
    employess =False                   
    driver.get(url)
    jobs = []


    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(4)

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
        
        if not clickable: 
            try:                
                WebDriverWait(driver, slp_time).until(
                EC.presence_of_element_located((By.ID, "filter_minSalary"))).click()    
                
                WebDriverWait(driver, slp_time).until(
                EC.presence_of_element_located((By.XPATH,'.//div[@class="checkboxBox"]'))).click()  
                WebDriverWait(driver, slp_time).until(
                EC.presence_of_element_located((By.XPATH, './/button[@class="applybutton gd-btn gd-btn-link gradient gd-btn-2 gd-btn-sm"]'))).click()  
                clickable = True 
                print('Salary filter is working')
            except TimeoutException:
                print('Can not find Salary filter')
                pass
            time.sleep(.1)
            
        if not employess: 
               try:
                   WebDriverWait(driver, slp_time).until(
                   EC.presence_of_element_located((By.XPATH,'.//div[@class="filter more expandable"]'))).click() 
                   
                   WebDriverWait(driver, slp_time).until(
                   EC.presence_of_element_located((By.XPATH,'.//div[@class="filter more expandable expanded"]//div[@id="filter_employerSizes"]'))).click() 
                   
                   WebDriverWait(driver, slp_time).until(
                   EC.presence_of_element_located((By.XPATH,'.//ul[@class="css-1dv4b0s ew8xong0"]//li[@value="5"]'))).click() 
                   
                   time.sleep(.1)   
                   
                   WebDriverWait(driver, slp_time).until(
                   EC.presence_of_element_located((By.XPATH,'.//div[@class="allDropdowns"]//div[@class="filter more expandable expanded applied"]'))).click() 
                  
                   employess = True 
                   print('Company size filter working')
               except (NoSuchElementException,TimeoutException,StaleElementReferenceException,ElementNotInteractableException):               
                   print('Company filter failed')     

                   pass

        
        #Going through each job in this page
        try:
             job_buttons = WebDriverWait(driver, slp_time,ignored_exceptions=ignored_exceptions).until(
             EC.visibility_of_all_elements_located((By.CLASS_NAME,'jl')))
             
             #job_buttons = driver.find_elements_by_class_name("jl")
        except: 
            pass
      
        
        #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            actions.move_to_element(job_button).perform()
            job_button.click()  #You might 
            time.sleep(1)
            collected_successfully = False
            
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
                    collected_successfully = True
                                       
                except (NoSuchElementException,TimeoutException,ElementNotInteractableException,StaleElementReferenceException):
                    job_description = -1
                    

            try:
                salary_estimate = driver.find_element_by_xpath('.//span[@class="css-1uyte9r css-hca4ks e1wijj242"]').text
            except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            except (NoSuchElementException,ElementNotInteractableException):
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                tab_click=WebDriverWait(driver, slp_time,ignored_exceptions=ignored_exceptions).until(
                EC.element_to_be_clickable((By.XPATH,'.//span[text()="Company"]')))
                tab_click.click()
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

              

            except (NoSuchElementException,TimeoutException,ElementClickInterceptedException,ElementNotInteractableException,StaleElementReferenceException):  #Rarely, some job postings do not have the "Company" tab.
                
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
                rating_click.click()
                try:
                        ceo = driver.find_element_by_xpath('.//*[@id="RatingContainer"]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]').text
                                       
                except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):                      
                       ceo = -1
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
                       
                       work_life_balance = -1
            except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):  #Rarely, some job postings do not have the "Company" tab.
                
                    compensation_benefits = -1
                    culture_values = -1
                    career_opportunities = -1
                    work_life_balance = -1
                    ceo = -1
            if verbose:
                
                print("Compensation & Benefits: {}".format(compensation_benefits))
                print("Culture Values: {}".format(culture_values))
                print("Career Opportunities {}".format(career_opportunities))
                print("WorkLife Balance: {}".format(work_life_balance))
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
            
            
            
            
            
            })
            #add job to jobs

        #Clicking on the "next page" button
        try:
            nextpages = WebDriverWait(driver, slp_time).until(
                EC.presence_of_element_located((By.XPATH, './/li[@class="next"]//a')))
            actions.move_to_element(nextpages).perform()
            nextpages.click()
            #driver.find_element_by_xpath('.//li[@class="next"]//a').click()
            driver.refresh()
            drop_box = WebDriverWait(driver, slp_time).until(
                   EC.presence_of_element_located((By.XPATH,'.//div[@class="allDropdowns"]//div[@class="filter more expandable expanded applied"]')))
            drop_box.click()
            
        except (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException):
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            #break
            pass

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.