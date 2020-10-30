#!/usr/bin/env python
# coding: utf-8

# # Campaign Contribution Data
# - consolidating three files into one
# - cleaning the data
# - adding column for party ie: democrat, republican etc
# - adding column for state

# In[1]:


# Dependencies
import re
import pandas as pd
import numpy as np
import requests
import os
import json
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
from IPython.core.display import HTML
from datetime import date, datetime


# In[2]:


contributions_2016 = pd.read_csv('campaign_contribution_2016.csv')
contributions_2018 = pd.read_csv('campaign_contribution_2018.csv')
stateName = pd.read_csv('stateAbbrv.csv')


# In[3]:


contributions_2016 =  contributions_2016.drop(contributions_2016.index[52])


# In[4]:


contributions_2016.tail(51)


# In[5]:


len(contributions_2016)


# In[6]:


stripList = contributions_2016['Representative']
namesNoAstrick = []
for i in stripList:
    namesNoAstrick.append(i[:-1])


# In[7]:


len(namesNoAstrick)


# In[8]:


namesNoAstrick[0]


# In[9]:


namesNoAstrick[-4] = 'SandersBernie Sanders (D-VT)'


# In[10]:


# counter =0
# while counter < len(namesNoAstrick):
#     if "N00009975&cycle=2016" in namesNoAstrick[counter]:
#         print(counter)
#     else:
#         counter += 1


# In[11]:


namesNoAstrick[51]


# In[12]:


def stripNames(stripList):
    state = []
    fullName = []
    party = []
    state = []
    for i in stripList:
        counter = 0
        for j in i:
            counter += 1
            if j == '(':
                party.append(i[counter:-1])
                state.append(i[counter+2:-1])
                fullName.append(i[:counter-2])
            elif '(' not in i:
                print(i)
    return fullName, state, party


# In[13]:


listName = stripNames(namesNoAstrick)


# In[14]:


len(listName[0])


# In[15]:


def cleanName(string):
    i = 1
    while i < len(string):
        if string[i] >= 'A' and string[i] <= 'Z':
            #print(i)
            return string[i:]
        else:
            i+= 1


# In[16]:


#listName[1]


# In[17]:


cleanedName = []
for i in listName[0]:
    cleanedName.append(cleanName(i))
#cleanedName


# In[18]:


party = []
for i in listName[2]:
    if 'D' in i:
        party.append('D')
    elif 'R' in i:
        party.append('R')
    else:
        party.append('I')


# In[19]:


matchList = listName[1]
#matchList


# In[20]:


AP = []
for i in stateName['Abbrev']:
    if i[-1] == '.':
        AP.append(i[:-1])
    else:
        AP.append(i)


# In[21]:


stateName['AP'] = AP


# In[22]:


abbrev = stateName['AP']
abbrev = abbrev.tolist()
#abbrev
fullState = (stateName['State']).tolist()
shortAbbrev = (stateName['Code']).tolist()
fullStateLower = []
for i in fullState:
    fullStateLower.append(i.lower())
stateDict = dict(zip(shortAbbrev, fullStateLower))


# In[23]:


otherDict = dict(zip(AP, fullStateLower))
stateName['lower'] = fullStateLower


# In[24]:


len(matchList)#[95:]


# In[25]:


#stateDict


# In[26]:


#Matches the strings that have AP style abbreviation with full statenames
def getMatch(string):
    for key, value in otherDict.items():
        if value.startswith(string):
            return value


# In[27]:


#Calling getMatch with matchList input from csv
holder = []
counter = 0
for i in matchList:
    #print(i)
    i = i.lower()
    if (i == 'fla'):
        holder.append('florida')
        counter += 1
    elif (i == 'wva'):
        holder.append('west virginia')
        counter += 1
    elif len(i) > 2:
        holder.append(getMatch(i))
        counter += 1
    elif len(i) == 2:
        holder.append(i.upper())
        counter += 1
    else:
        holder.append('None')
        print(f'{counter}: no match')
        counter += 1
#holder


# In[28]:


#Matches the full state names to abbreviations
def getMatch2(string):
    for key, value in stateDict.items():
        if value.startswith(string):
            return key


# In[29]:


#Calling getMatch2 with holder from getMatch
renamedState = []
for i in holder:
    if len(i) == 2:
        renamedState.append(i)
    else:
        renamedState.append(getMatch2(i))


# In[30]:


len(renamedState)


# In[31]:


Total_Raised = []
for i in contributions_2016['Total Raised']:
    Total_Raised.append(int(i[1:]))


# In[32]:


len(Total_Raised)


# In[33]:


contributions_2016['Total_Raised'] = Total_Raised
contributions_2016['State'] = renamedState
contributions_2016['Party'] = party
contributions_2016['Name'] = cleanedName


# In[34]:


contributions_2016 = contributions_2016.drop(['Representative', 'Office Running For', 'Total Raised'], axis = 1)


# In[35]:


contributions_2016 = contributions_2016[['Name', 'State', 'Party', 'Total_Raised']]


# In[36]:


contributions_2016


# In[37]:


contributions_2016.to_csv('contributions_2016.csv', index = False)


# In[38]:


get_ipython().system('jupyter nbconvert --to python campaignContribution2016.ipynb')


# In[ ]:




