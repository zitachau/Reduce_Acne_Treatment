#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 19:11:05 2021

@author: zitachau
"""

import requests
import pandas as pd 
import json


# Example of how to pull date from a specific date

date = "2021-01-25"
myapi = 'your api key'

url = 'http://api.weatherapi.com/v1/history.json?key=' + myapi + '&q=yourzipcode&dt=' + date 

response = requests.get(url)
data = response.text

jsonData = json.loads(data)

#Parsing the Data from the Response
metaData1 = pd.DataFrame(jsonData['location'], index=[0])
metaData1 = metaData1.drop(columns=['localtime_epoch','localtime'])

metaData2 = pd.DataFrame({'date': jsonData['forecast']['forecastday'][0]['date']}, index=[0])

metaData3 = jsonData['forecast']['forecastday'][0]['day']
metaData3.pop('condition', None)
metaData3 = pd.DataFrame(metaData3, index=[0])

#Create a new dataframe
metadata_combined = pd.concat([metaData1, metaData2, metaData3], axis=1)
metadata_combined = metadata_combined.set_index('date')




# How to turn this into a function where we can insert a specific date: 

def dataPull(date):
    api = 'myapi'
    url = 'http://api.weatherapi.com/v1/history.json?key=' + api + '&q=yourzipcode&dt=' + date
    response = requests.get(url)
    data = response.text
    jsonData = json.loads(data)
    metaData1 = pd.DataFrame(jsonData['location'], index=[0])
    metaData1 = metaData1.drop(columns=['localtime_epoch','localtime'])
    metaData2 = pd.DataFrame({'date': jsonData['forecast']['forecastday'][0]['date']}, index=[0])
    metaData3 = jsonData['forecast']['forecastday'][0]['day']
    metaData3.pop('condition', None)
    metaData3 = pd.DataFrame(metaData3, index=[0])
    metadata_combined = pd.concat([metaData1, metaData2, metaData3], axis=1)
    metadata_combined = metadata_combined.set_index('date')
    return metadata_combined


test = dataPull('2021-01-26')




# What about specific dates?
#### NOTE - the free tier APA can only go back in time 7 days,

listofDates = ['2021-01-25','2021-01-26', '2021-01-27', '2021-01-28']
returnedDataframes = []

for x in listofDates:
    responsedf = dataPull(x)
    returnedDataframes.append(responsedf)


merged_response = pd.concat(returnedDataframes)



