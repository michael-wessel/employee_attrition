'''
Chi Squared with a 2x2 Contingency

H0: Gender and Attrition are independent.
H1: Gender and Attrition are not independent.

'''
from scipy.stats import chi2_contingency
import pandas as pd
import numpy as np
import os
os.chdir('C:/Users/micwessel/Projects/employee_attrition')
pd.set_option('display.max_rows', None)

df = pd.read_csv('data/data.csv')
df['terminationdate_key'] = np.where(df['terminationdate_key']=='1/1/1900', np.nan, df['terminationdate_key'])
df[['recorddate_key', 'birthdate_key', 'orighiredate_key', 'terminationdate_key']] = df[['recorddate_key', 'birthdate_key', 'orighiredate_key', 'terminationdate_key']].astype('datetime64[ns]')
df['status_recode'] = np.where(df['STATUS']=='ACTIVE', 0, 1)

recoded_df = df.groupby(by=['EmployeeID', 'gender_full'])['status_recode'].sum()
recoded_df = recoded_df.reset_index()
recoded_df.head()

males_df = recoded_df.loc[recoded_df['gender_full'] == 'Male']
males_df.head()
males = males_df['EmployeeID'].nunique()
males # Total number of males in the dataset
male_attritions = males_df['status_recode'].sum()
male_attritions # Male attrition rate
male_nonattritions = males - male_attritions
male_nonattritions

females_df = recoded_df.loc[recoded_df['gender_full'] == 'Female']
females_df.head()
females = females_df['EmployeeID'].nunique()
females # Total number of males in the dataset
female_attritions = females_df['status_recode'].sum()
female_attritions # Male attrition rate
female_nonattritions = females - female_attritions
female_nonattritions

observed = np.array([[male_attritions, male_nonattritions] , [female_attritions, female_nonattritions]])
chi_val, p_val, dof, expected = chi2_contingency(observed)
chi_val, p_val, dof, expected

'''
The p value obtained from the chi-square test for independence is significant (p < 0.05), 
and therefore, we can conclude that there is a significant association between gender 
(male and female) with attrition outcome (attrition and non-attrition)
'''