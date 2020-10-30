#!/usr/bin/env python
# coding: utf-8

# # Campaign Contribution Data
# - consolidating three files into one
# - cleaning the data
# - adding column for party ie: democrat, republican etc
# - adding column for state

# In[24]:


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


# In[25]:


contributions_2016 = pd.read_csv('campaign_contribution_2016.csv')
contributions_2018 = pd.read_csv('campaign_contribution_2018.csv')
stateName = pd.read_csv('stateAbbrv.csv')


# In[26]:


contributions_2016 =  contributions_2016.drop(contributions_2016.index[52])


# In[27]:


contributions_2016['Representative'][2] = "ConnellMitch McConnell (R-Ky)"


# In[28]:


len(contributions_2016)


# In[29]:


stripList = contributions_2016['Representative']
namesNoAstrick = []
for i in stripList:
    namesNoAstrick.append(i[:-1])


# In[30]:


len(namesNoAstrick)


# In[31]:


namesNoAstrick[0]


# In[32]:


namesNoAstrick[-4] = 'SandersBernie Sanders (D-VT)'


# In[33]:


# counter =0
# while counter < len(namesNoAstrick):
#     if "N00009975&cycle=2016" in namesNoAstrick[counter]:
#         print(counter)
#     else:
#         counter += 1


# In[34]:


namesNoAstrick[51]


# In[35]:


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


# In[36]:


listName = stripNames(namesNoAstrick)


# In[37]:


len(listName[0])


# In[38]:


def cleanName(string):
    i = 1
    while i < len(string):
        if string[i] >= 'A' and string[i] <= 'Z':
            #print(i)
            return string[i:]
        else:
            i+= 1


# In[39]:


#listName[1]


# In[40]:


cleanedName = []
for i in listName[0]:
    cleanedName.append(cleanName(i))
cleanedName


# In[41]:


party = []
for i in listName[2]:
    if 'D' in i:
        party.append('D')
    elif 'R' in i:
        party.append('R')
    else:
        party.append('I')


# In[42]:


matchList = listName[1]
#matchList


# In[43]:


AP = []
for i in stateName['Abbrev']:
    if i[-1] == '.':
        AP.append(i[:-1])
    else:
        AP.append(i)


# In[44]:


stateName['AP'] = AP


# In[45]:


abbrev = stateName['AP']
abbrev = abbrev.tolist()
#abbrev
fullState = (stateName['State']).tolist()
shortAbbrev = (stateName['Code']).tolist()
fullStateLower = []
for i in fullState:
    fullStateLower.append(i.lower())
stateDict = dict(zip(shortAbbrev, fullStateLower))


# In[46]:


otherDict = dict(zip(AP, fullStateLower))
stateName['lower'] = fullStateLower


# In[47]:


len(matchList)#[95:]


# In[48]:


#stateDict


# In[49]:


#Matches the strings that have AP style abbreviation with full statenames
def getMatch(string):
    for key, value in otherDict.items():
        if value.startswith(string):
            return value


# In[50]:


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


# In[51]:


#Matches the full state names to abbreviations
def getMatch2(string):
    for key, value in stateDict.items():
        if value.startswith(string):
            return key


# In[52]:


#Calling getMatch2 with holder from getMatch
renamedState = []
for i in holder:
    if len(i) == 2:
        renamedState.append(i)
    else:
        renamedState.append(getMatch2(i))


# In[53]:


len(renamedState)


# In[54]:


Total_Raised = []
for i in contributions_2016['Total Raised']:
    Total_Raised.append(int(i[1:]))


# In[55]:


len(Total_Raised)


# In[56]:


contributions_2016['Total_Raised'] = Total_Raised
contributions_2016['State'] = renamedState
contributions_2016['Party'] = party
contributions_2016['Name'] = cleanedName


# In[57]:


contributions_2016 = contributions_2016.drop(['Representative', 'Office Running For', 'Total Raised'], axis = 1)


# In[58]:


contributions_2016 = contributions_2016[['Name', 'State', 'Party', 'Total_Raised']]


# In[59]:


contributions_2016


# In[60]:


contributions_2016.to_csv('contributions_2016.csv', index = False)


# In[61]:


get_ipython().system('jupyter nbconvert --to python campaignContribution2016.ipynb')


# In[ ]:




