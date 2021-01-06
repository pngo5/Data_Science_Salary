# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 18:19:18 2020

@author: phatn
"""

import web_scraping_MAIN as gs
import pandas as pd

path ="C:/Users/phatn/Data_Science_Salary/chromedriver"

df = gs.get_jobs('data scientist', 'United States', 15, False, path, 15,True)
#df = gs.get_jobs2('data scientist',300,False,path,30)
