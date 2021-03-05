from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
import os
os.chdir('C:/Users/micwessel/Projects/employee_attrition')
pd.set_option('display.max_rows', None)

df = pd.read_csv('data/data.csv')
df['terminationdate_key'] = np.where(df['terminationdate_key']=='1/1/1900', np.nan, df['terminationdate_key'])
df[['recorddate_key', 'birthdate_key', 'orighiredate_key', 'terminationdate_key']] = df[['recorddate_key', 'birthdate_key', 'orighiredate_key', 'terminationdate_key']].astype('datetime64[ns]')


# Females
female_reg = df.loc[df['gender_full'] == 'Female']
female_reg = female_reg.groupby(by=['STATUS_YEAR', 'termreason_desc'])['EmployeeID'].nunique()
female_reg = female_reg.unstack('termreason_desc')
female_reg = female_reg.fillna(0)
female_reg.rename(columns = {'Resignaton':'Resignation'}, inplace = True)
female_reg['Total Departures'] = female_reg['Layoff'] + female_reg['Resignation'] + female_reg['Retirement']
female_reg['Gender'] = 'Male'
female_reg = female_reg.reset_index()
a_m = (female_reg['Not Applicable'].rolling(min_periods=1, window=2).sum())/2
b_m = df[(df['STATUS_YEAR'] == 2006) & (df['orighiredate_key'] <= '2005-12-31') & (df['gender_full'] == 'Male')].nunique()
c_m = female_reg.at[0,'Not Applicable']
d_m = (b_m['EmployeeID'] + c_m) / 2
female_reg.loc[female_reg['STATUS_YEAR'] != 2006, 'Average Number of Employees'] = a_m
female_reg.loc[female_reg['STATUS_YEAR'] == 2006, 'Average Number of Employees'] = d_m
female_reg['Total Rate'] = (female_reg['Total Departures'] / female_reg['Average Number of Employees'])
female_reg['Resignation Rate'] = (female_reg['Resignation'] / female_reg['Average Number of Employees'])
female_reg['Retirement Rate'] = (female_reg['Retirement'] / female_reg['Average Number of Employees'])
female_reg['Layoff Rate'] = (female_reg['Layoff'] / female_reg['Average Number of Employees'])
female_reg['Voluntary Rate'] = ((female_reg['Resignation'] + female_reg['Retirement']) / female_reg['Average Number of Employees'])

# Female line of best fit - prediciton
df = female_reg
# Line of best fit for the selected column TODO: Insert callback value here and style
Y=df['Total Rate']
X=df.index

# regression
reg = LinearRegression().fit(np.vstack(X), Y)
df['bestfit'] = reg.predict(np.vstack(X))

# plotly figure setup
fig=go.Figure()
fig.add_trace(go.Bar(name='X vs Y', x=X, y=Y))
fig.add_trace(go.Scatter(name='line of best fit', x=X, y=df['bestfit'], mode='lines'))

fig.show()


# Males
male_reg = df.loc[df['gender_full'] == 'Male']
male_reg = male_reg.groupby(by=['STATUS_YEAR', 'termreason_desc'])['EmployeeID'].nunique()
male_reg = male_reg.unstack('termreason_desc')
male_reg = male_reg.fillna(0)
male_reg.rename(columns = {'Resignaton':'Resignation'}, inplace = True)
male_reg['Total Departures'] = male_reg['Layoff'] + male_reg['Resignation'] + male_reg['Retirement']
male_reg['Gender'] = 'Male'
male_reg = male_reg.reset_index()
a_m = (male_reg['Not Applicable'].rolling(min_periods=1, window=2).sum())/2
b_m = df[(df['STATUS_YEAR'] == 2006) & (df['orighiredate_key'] <= '2005-12-31') & (df['gender_full'] == 'Male')].nunique()
c_m = male_reg.at[0,'Not Applicable']
d_m = (b_m['EmployeeID'] + c_m) / 2
male_reg.loc[male_reg['STATUS_YEAR'] != 2006, 'Average Number of Employees'] = a_m
male_reg.loc[male_reg['STATUS_YEAR'] == 2006, 'Average Number of Employees'] = d_m
male_reg['Total Rate'] = (male_reg['Total Departures'] / male_reg['Average Number of Employees'])
male_reg['Resignation Rate'] = (male_reg['Resignation'] / male_reg['Average Number of Employees'])
male_reg['Retirement Rate'] = (male_reg['Retirement'] / male_reg['Average Number of Employees'])
male_reg['Layoff Rate'] = (male_reg['Layoff'] / male_reg['Average Number of Employees'])
male_reg['Voluntary Rate'] = ((male_reg['Resignation'] + male_reg['Retirement']) / male_reg['Average Number of Employees'])

# Male line of best fit - prediciton
df = male_reg

# Line of best fit for the selected column TODO: Insert callback value here and style
Y=df['Total Rate']
X=df.index

# regression
reg = LinearRegression().fit(np.vstack(X), Y)
df['bestfit'] = reg.predict(np.vstack(X))

# plotly figure setup
fig=go.Figure()
fig.add_trace(go.Bar(name='X vs Y', x=X, y=Y.values))
fig.add_trace(go.Scatter(name='line of best fit', x=X, y=df['bestfit'], mode='lines'))

# plotly figure layout
fig.update_layout(xaxis_title = 'Departure Rate', yaxis_title = 'Year')

fig.show()