# -*- coding: utf-8 -*-
"""
Created on 12/21/2020

@Phat Ngo
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

#https://github.com/arapfaik/scraping-glassdoor-selenium/blob/master/glassdoor%20scraping.ipynb

def get_jobs(keyword, num_jobs, verbose,path,slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1520, 1500)
#For GA    
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=S&locId=3426&jobType="
#For     
    
   # url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []
    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
        
        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)
    
        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)
#-------------------------------------------Close the pop-up, and move on with the search.
#-------------------------------------------Created a variable call clickable, and employ for it to go alone with the loop.
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
                driver.find_element_by_id('filter_minSalary').click()
                driver.find_element_by_xpath('.//div[@class="checkboxBox"]').click()
                driver.find_element_by_xpath('.//button[@class="applybutton gd-btn gd-btn-link gradient gd-btn-2 gd-btn-sm"]').click()
                clickable = True 
                print('Salary filter is working')
            except NoSuchElementException:
                print('Can not find Salary filter')
                pass
        #filter by 5000 Plus employees   
        while not employess: 
            try:
                driver.find_element_by_xpath('.//div[@class="filter more expandable"]').click()
                driver.find_element_by_xpath('.//div[@class="filter more expandable expanded"]//div[@id="filter_employerSizes"]').click()
                driver.find_element_by_xpath('.//ul[@class="css-1dv4b0s ew8xong0"]//li[@value="5"]').click()
                time.sleep(.05)             
                driver.find_element_by_xpath('.//div[@class="allDropdowns"]//div[@class="filter more expandable expanded applied"]').click()
                employess = True 
                print('Company size filter working')
            except NoSuchElementException:               
                print('Company filter failed')
                driver.find_element_by_xpath('.//div[@class="allDropdowns"]//div[@class="filter more expandable expanded applied"]').click()
                employess = True 
                
                pass
        
 #------------------------------------------       
        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element_by_xpath('.//span[@class="css-1uyte9r css-hca4ks e1wijj242"]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            except NoSuchElementException:
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
                driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

                #try:
                    #<div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    #</div>
               #     headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
               # except NoSuchElementException:
               #     headquarters = -1

                try:
                    size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1
#-------------------------------- The competitor part have been remove from the company pages
               # try:
               #     competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
               # except NoSuchElementException:
               #     competitors = -1
#-------------------------------- Going to another pages and getting the ceo name                 

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
               # headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
               # competitors = -1
            try:
                driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="rating"]').click()
                driver.execute_script("window.scrollTo(1200, document.body.scrollHeight);")
                #Sleeping for .1 to make sure its loading correctly #MAKE CHANGES BASED ON INTERNET SPEED
                time.sleep(.4)
                try:
                    ceo= driver.find_element_by_xpath('//*[@id="RatingContainer"]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]').text
                except NoSuchElementException:
                     ceo = -1
                
                #Getting the rating of the company
                try:
                    compensation_benefits= driver.find_element_by_xpath('.//strong[text()="Culture & Values"]//following-sibling::*').text
                except NoSuchElementException:
                     compensation_benefits = -1
                try:
                    culture_values = driver.find_element_by_xpath('.//strong[text()="Compensation & Benefits"]//following-sibling::*').text
                except NoSuchElementException:
                       culture_values = -1
                try:
                    career_opportunities = driver.find_element_by_xpath('.//strong[text()="Career Opportunities"]//following-sibling::*').text
                except NoSuchElementException:
                       career_opportunities = -1
                try:
                    work_life_balance = driver.find_element_by_xpath('.//strong[text()="Work/Life Balance"]//following-sibling::*').text
                except NoSuchElementException:
                       work_life_balance = -1
                
                
            except NoSuchElementException:
                    compensation_benefits = -1
                    culture_values = -1
                    career_opportunities = -1
                    work_life_balance = -1
                    ceo = -1

                
            if verbose:
               # print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Compensation & Benefits: {}".format(compensation_benefits))
                print("Culture & Values: {}".format(culture_values)) 
                print("Career Opportunities: {}".format(career_opportunities))
                print("Work/Life Balance: {}".format(work_life_balance))
                print("Ceo : {}".format(ceo))
               # print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Company Name" : company_name,
            "Location" : location,
          #  "Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "CEO" : ceo,
            "Overall Rating" : rating,
            "Culture & Values" : culture_values,
            "Compensation & Benefits": compensation_benefits,
            "Career Opportunities:": career_opportunities,
            "Work/Life Balance" : work_life_balance,
            #"Competitors" : competitors
            })
            #add job to jobs

        #Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.

        
        