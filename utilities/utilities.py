import pandas as pd
import numpy as np
import os
os.chdir('C:/Users/micha/Projects/employee_attrition')
pd.set_option('display.max_rows', None)

# Read in the sample data and take a look.
df = pd.read_csv('data/data.csv')
# df.head()
# df.dtypes

# Blank values in terminationdate_key are listed as '1/1/1900' so I chose to replace them with NaN via numpy.
df['terminationdate_key'] = np.where(df['terminationdate_key']=='1/1/1900', np.nan, df['terminationdate_key'])
# df.head()

# After replacing null values, I converted all date columns to datetime format. 
# This addressed the 'recorddate_key' format that included blank H:MM values.
df[['recorddate_key', 'birthdate_key', 'orighiredate_key', 'terminationdate_key']] = df[['recorddate_key', 'birthdate_key', 'orighiredate_key', 'terminationdate_key']].astype('datetime64[ns]')
# df.dtypes

# I first looked at females
females_df = df.loc[df['gender_full'] == 'Female']
females_df = females_df.groupby(by=['STATUS_YEAR', 'termreason_desc'])['EmployeeID'].nunique()
females_df = females_df.unstack('termreason_desc')
females_df = females_df.fillna(0)
females_df.rename(columns = {'Resignaton':'Resignation'}, inplace = True)
females_df['Total Departures'] = females_df['Layoff'] + females_df['Resignation'] + females_df['Retirement']
females_df['Gender'] = 'Female'
females_df = females_df.reset_index()

# Employee attrition formula = Departures - Average Number of Employees (n) * 100
# Average Number of Employees formula (n) = Employees at start of period (n0) + Employee at end of period (n1) / 2
# Average number of female employees per year (n = n0 + n1)
# n0 logic for 2016 ---> status year = 2006 & hire date <= 12/31/2005
# n1 logic = "Not Applicable" for status year
a_f = (females_df['Not Applicable'].rolling(min_periods=1, window=2).sum())/2
b_f = df[(df['STATUS_YEAR'] == 2006) & (df['orighiredate_key'] <= '2005-12-31') & (df['gender_full'] == 'Female')].nunique()
c_f = females_df.at[0,'Not Applicable']
d_f = (b_f['EmployeeID'] + c_f) / 2
females_df.loc[females_df['STATUS_YEAR'] != 2006, 'Average Number of Employees'] = a_f
females_df.loc[females_df['STATUS_YEAR'] == 2006, 'Average Number of Employees'] = d_f

# Female Rate calculations
females_df['Total Rate'] = (females_df['Total Departures'] / females_df['Average Number of Employees']).map('{:.2%}'.format)
females_df['Resignation Rate'] = (females_df['Resignation'] / females_df['Average Number of Employees']).map('{:.2%}'.format)
females_df['Retirement Rate'] = (females_df['Retirement'] / females_df['Average Number of Employees']).map('{:.2%}'.format)
females_df['Layoff Rate'] = (females_df['Layoff'] / females_df['Average Number of Employees']).map('{:.2%}'.format)
females_df['Voluntary Rate'] = ((females_df['Resignation'] + females_df['Retirement']) / females_df['Average Number of Employees']).map('{:.2%}'.format)
# females_df

# Then I looked at males
males_df = df.loc[df['gender_full'] == 'Male']
males_df = males_df.groupby(by=['STATUS_YEAR', 'termreason_desc'])['EmployeeID'].nunique()
males_df = males_df.unstack('termreason_desc')
males_df = males_df.fillna(0)
males_df.rename(columns = {'Resignaton':'Resignation'}, inplace = True)
males_df['Total Departures'] = males_df['Layoff'] + males_df['Resignation'] + males_df['Retirement']
males_df['Gender'] = 'Male'
males_df = males_df.reset_index()

# Employee attrition formula = Departures - Average Number of Employees (n) * 100
# Average Number of Employees formula (n) = Employees at start of period (n0) + Employee at end of period(N1) / 2
# Average number of female employees per year (n = n0 + n1)
# n0 logic for 2016 ---> status year = 2006 & hire date <= 12/31/2005
# n1 logic = "Not Applicable" for status year
a_m = (males_df['Not Applicable'].rolling(min_periods=1, window=2).sum())/2
b_m = df[(df['STATUS_YEAR'] == 2006) & (df['orighiredate_key'] <= '2005-12-31') & (df['gender_full'] == 'Male')].nunique()
c_m = males_df.at[0,'Not Applicable']
d_m = (b_m['EmployeeID'] + c_m) / 2
males_df.loc[males_df['STATUS_YEAR'] != 2006, 'Average Number of Employees'] = a_m
males_df.loc[males_df['STATUS_YEAR'] == 2006, 'Average Number of Employees'] = d_m

# Rate calculations
males_df['Total Rate'] = (males_df['Total Departures'] / males_df['Average Number of Employees']).map('{:.2%}'.format)
males_df['Resignation Rate'] = (males_df['Resignation'] / males_df['Average Number of Employees']).map('{:.2%}'.format)
males_df['Retirement Rate'] = (males_df['Retirement'] / males_df['Average Number of Employees']).map('{:.2%}'.format)
males_df['Layoff Rate'] = (males_df['Layoff'] / males_df['Average Number of Employees']).map('{:.2%}'.format)
males_df['Voluntary Rate'] = ((males_df['Resignation'] + males_df['Retirement']) / males_df['Average Number of Employees']).map('{:.2%}'.format)
# males_df

## Calculation validation
# male_hires = df[(df['orighiredate_key'] > '2005-12-31') & (df['orighiredate_key'] <= '2006-12-31') & (df['gender_full'] == 'Male')].nunique()
# male_hires['EmployeeID'] + b_m - 74

# Total Average Employee Count 
female_start = b_f['EmployeeID']
female_end = females_df.at[9,'Not Applicable']
female_total_average = (female_start + female_end) / 2
male_start = b_m['EmployeeID']
male_end = males_df.at[9,'Not Applicable']
male_total_average = (male_start + male_end) / 2

# Total Departure Breakdown Counts
female_resignations_count = females_df['Resignation'].sum()
female_retirements_count = females_df['Retirement'].sum()
female_layoffs_count = females_df['Layoff'].sum()
female_voluntary_count = female_resignations_count + female_retirements_count
male_resignations_count = males_df['Resignation'].sum()
male_retirements_count = males_df['Retirement'].sum()
male_layoffs_count = males_df['Layoff'].sum()
male_voluntary_count = male_resignations_count + male_retirements_count

# Total Departure Breakdown Rates
female_resignations_rate = female_resignations_count / female_total_average
female_retirements_rate = female_retirements_count / female_total_average
female_layoffs_rate = female_layoffs_count / female_total_average
female_voluntary_rate = female_voluntary_count / female_total_average
male_resignations_rate = male_resignations_count / male_total_average
male_retirements_rate = male_retirements_count / male_total_average
male_layoffs_rate = male_layoffs_count / male_total_average
male_voluntary_rate = male_voluntary_count / male_total_average

# Total Rates DataFrame
final_rates = pd.DataFrame()
final_rates['Gender'] = ['Male', 'Female']
final_rates['Average Employee Count'] = [male_total_average, female_total_average]
final_rates['Resignation Count'] = [male_resignations_count, female_resignations_count]
final_rates['Resignation Rate'] = [male_resignations_rate, female_resignations_rate]
final_rates['Resignation Rate'] = final_rates['Resignation Rate'].map('{:.2%}'.format)
final_rates['Retirement Count'] = [male_retirements_count, female_retirements_count]
final_rates['Retirement Rate'] = [male_retirements_rate, female_retirements_rate]
final_rates['Retirement Rate'] = final_rates['Retirement Rate'].map('{:.2%}'.format)
final_rates['Layoff Count'] = [male_layoffs_count, female_layoffs_count]
final_rates['Layoff Rate'] = [male_layoffs_rate, female_layoffs_rate]
final_rates['Layoff Rate'] = final_rates['Layoff Rate'].map('{:.2%}'.format) 
final_rates['Voluntary Count'] = [male_voluntary_count, female_voluntary_count]
final_rates['Voluntary Rate'] = [male_voluntary_rate, female_voluntary_rate]
final_rates['Voluntary Rate'] = final_rates['Voluntary Rate'].map('{:.2%}'.format) 
# final_rates

table_rates = pd.DataFrame()
table_rates['Departure Metric'] = [
    'Avg. Employee Count (n)',
    'Resignation Count',
    'Resignation Rate',
    'Retirement Count',
    'Retirement Rate',
    'Layoff Count',
    'Layoff Rate',
    'Voluntary Count',
    'Voluntary Rate',
]
table_rates['Male'] = [
    male_total_average, 
    male_resignations_count,
    "{:.2%}".format(male_resignations_rate),
    male_retirements_count,
    "{:.2%}".format(male_retirements_rate),
    male_layoffs_count,
    "{:.2%}".format(male_layoffs_rate),
    male_voluntary_count,
    "{:.2%}".format(male_voluntary_rate)
]
table_rates['Female'] = [
    female_total_average, 
    female_resignations_count,
    "{:.2%}".format(female_resignations_rate),
    female_retirements_count,
    "{:.2%}".format(female_retirements_rate),
    female_layoffs_count,
    "{:.2%}".format(female_layoffs_rate),
    female_voluntary_count,
    "{:.2%}".format(female_voluntary_rate)
]
# table_rates

# Line plot dataframe for graph
frames = [females_df, males_df]
plot_df = pd.concat(frames)