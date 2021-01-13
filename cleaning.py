# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 07:29:27 2021

@author: phatn
"""

import pandas as pd

df= pd.read_csv("glassdoor_jobs_12_20.csv")

#salary parsing 
#Company name text only
#state field
# age of company 
#parsing of description (python, etc...)

#Removing all the -1 in the data
df = df[df['Job Description'] != '-1']
df = df[df['Job Title']!= '-1']

salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
removed_km=salary.apply(lambda x: x.replace('K',' ').replace('$',' '))

#Getting the min, and the max salary, and also changing it into a int. 
#The values are string at the moment
df['min_salary']=removed_km.apply(lambda x: int(x.split('-')[0]))
df['max_salary']=removed_km.apply(lambda x: int(x.split('-')[1]))
df['avg_salary']=(df.min_salary+df.max_salary)/2

#removing all the -1
df['company_overall_rating_filter_txt'] = df.apply(lambda x: x['Company Name'] if x['Overall Rating'] < 0 else x['Company Name'][:-3], axis=1)

#getting the age of the company
df['age']= df.Founded.apply(lambda x: x if x < 1 else 2020 -x )