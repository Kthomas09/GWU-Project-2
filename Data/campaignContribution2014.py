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


contributions_2014 = pd.read_csv('campaign_contribution_2014.csv')
contributions_2016 = pd.read_csv('campaign_contribution_2016.csv')
contributions_2018 = pd.read_csv('campaign_contribution_2018.csv')
stateName = pd.read_csv('stateAbbrv.csv')


# In[3]:


contributions_2014


# In[4]:


stripList = contributions_2014['Representative']
namesNoAstrick = []
for i in stripList:
    namesNoAstrick.append(i[:-1])


# In[5]:


#namesNoAstrick


# In[6]:


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
    return fullName, state, party


# In[7]:


listName = stripNames(namesNoAstrick)


# In[8]:


def cleanName(string):
    i = 1
    while i < len(string):
        if string[i] >= 'A' and string[i] <= 'Z':
            #print(i)
            return string[i:]
        else:
            i+= 1


# In[9]:


#listName[0]


# In[10]:


cleanedName = []
for i in listName[0]:
    cleanedName.append(cleanName(i))
#cleanedName


# In[11]:


party = []
for i in listName[2]:
    if 'D' in i:
        party.append('D')
    elif 'R' in i:
        party.append('R')
    else:
        party.append('I')


# In[12]:


matchList = listName[1]
#matchList


# In[13]:


AP = []
for i in stateName['Abbrev']:
    if i[-1] == '.':
        AP.append(i[:-1])
    else:
        AP.append(i)


# In[14]:


stateName['AP'] = AP


# In[15]:


abbrev = stateName['AP']
abbrev = abbrev.tolist()
#abbrev
fullState = (stateName['State']).tolist()
shortAbbrev = (stateName['Code']).tolist()
fullStateLower = []
for i in fullState:
    fullStateLower.append(i.lower())
stateDict = dict(zip(shortAbbrev, fullStateLower))


# In[16]:


otherDict = dict(zip(AP, fullStateLower))
stateName['lower'] = fullStateLower


# In[17]:


matchList[:10]


# In[18]:


#stateDict


# In[19]:


#Matches the strings that have AP style abbreviation with full statenames
def getMatch(string):
    for key, value in otherDict.items():
        if value.startswith(string):
            return value


# In[20]:


#Calling getMatch with matchList input from csv
holder = []
for i in matchList:
    #print(i)
    i = i.lower()
    if (i == 'fla'):
        holder.append('florida')
    elif (i == 'wva'):
        holder.append('west virginia')
    elif len(i) > 2:
        holder.append(getMatch(i))
    elif len(i) == 2:
        holder.append(i.upper())
    else:
        print('none')
#holder


# In[21]:


#Matches the full state names to abbreviations
def getMatch2(string):
    for key, value in stateDict.items():
        if value.startswith(string):
            return key


# In[22]:


#Calling getMatch2 with holder from getMatch
renamedState = []
for i in holder:
    if len(i) == 2:
        renamedState.append(i)
    else:
        renamedState.append(getMatch2(i))


# In[23]:


Total_Raised = []
for i in contributions_2014['Total Raised']:
    Total_Raised.append(int(i[1:]))


# In[24]:


contributions_2014['Total_Raised'] = Total_Raised
contributions_2014['State'] = renamedState
contributions_2014['Party'] = party
contributions_2014['Name'] = cleanedName


# In[25]:


contributions_2014 = contributions_2014.drop(['Representative', 'Office Running For', 'Total Raised'], axis = 1)


# In[26]:


contributions_2014 = contributions_2014[['Name', 'State', 'Party', 'Total_Raised']]


# In[27]:


contributions_2014


# In[28]:


contributions_2014.to_csv('contributions_2014.csv', index=False)


# In[ ]:


get_ipython().system('jupyter nbconvert --to python campaignContribution2014.ipynb')


# In[ ]:




