# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 18:19:18 2020

@author: phatn
"""

import web_scraping_v2 as gs


path ="C:/Users/phatn/Data_Science_Salary/chromedriver"

df = gs.get_jobs('data scientist', 'Atlanta, GA', 500, False, path, 5,False)

df.to_csv('glassdoor_jobs_12_20.csv', index = False)