#!/usr/bin/env python
# coding: utf-8

# # Campaign Contribution Data
# - consolidating three files into one
# - cleaning the data
# - adding column for party ie: democrat, republican etc
# - adding column for state

# In[ ]:


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


# In[ ]:


contributions_2014 = pd.read_csv('campaign_contribution_2014.csv')
contributions_2016 = pd.read_csv('campaign_contribution_2016.csv')
contributions_2018 = pd.read_csv('campaign_contribution_2018.csv')
stateName = pd.read_csv('stateAbbrv.csv')


# In[ ]:


contributions_2014


# In[ ]:


stripList = contributions_2014['Representative']
namesNoAstrick = []
for i in stripList:
    namesNoAstrick.append(i[:-1])


# In[ ]:


#namesNoAstrick


# In[ ]:


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


# In[ ]:


listName = stripNames(namesNoAstrick)


# In[ ]:


def cleanName(string):
    i = 1
    while i < len(string):
        if string[i] >= 'A' and string[i] <= 'Z':
            #print(i)
            return string[i:]
        else:
            i+= 1


# In[ ]:


#listName[0]


# In[ ]:


cleanedName = []
for i in listName[0]:
    cleanedName.append(cleanName(i))
cleanedName[:10]


# In[ ]:


firstName = []
lastName = []
for i in cleanedName:
    j = 0
    while j < len(i):
        if i[j] == '.':
            #print(j)
            firstName.append(i[:j+1])
            lastName.append(i[j+2:])
            j += 1
        elif (i[j].isspace()) & ('.' not in i):
            firstName.append(i[:j])
            lastName.append(i[j:])
            j += 1
#         elif (i[j] == ' ') & (i[j+2] != '.'):
#             firstName.append(i[:j])
#             lastName.append(i[j:])
#             j += 1
        else:
            j+=1


# In[ ]:


party = []
fullPartyName = []
for i in listName[2]:
    if 'D' in i:
        party.append('D')
        fullPartyName.append('Democrat')
    elif 'R' in i:
        party.append('R')
        fullPartyName.append('Republican')
    else:
        party.append('I')
        fullPartyName.append('Independent/Other')


# In[ ]:


matchList = listName[1]
#matchList


# In[ ]:


AP = []
for i in stateName['Abbrev']:
    if i[-1] == '.':
        AP.append(i[:-1])
    else:
        AP.append(i)


# In[ ]:


stateName['AP'] = AP


# In[ ]:


abbrev = stateName['AP']
abbrev = abbrev.tolist()
#abbrev
fullState = (stateName['State']).tolist()
shortAbbrev = (stateName['Code']).tolist()
fullStateLower = []
for i in fullState:
    fullStateLower.append(i.lower())
stateDict = dict(zip(shortAbbrev, fullStateLower))


# In[ ]:


otherDict = dict(zip(AP, fullStateLower))
stateName['lower'] = fullStateLower


# In[ ]:


matchList[:10]


# In[ ]:


#stateDict


# In[ ]:


#Matches the strings that have AP style abbreviation with full statenames
def getMatch(string):
    for key, value in otherDict.items():
        if value.startswith(string):
            return value


# In[ ]:


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


# In[ ]:


#Matches the full state names to abbreviations
def getMatch2(string):
    for key, value in stateDict.items():
        if value.startswith(string):
            return key


# In[ ]:


#Calling getMatch2 with holder from getMatch
renamedState = []
for i in holder:
    if len(i) == 2:
        renamedState.append(i)
    else:
        renamedState.append(getMatch2(i))


# In[ ]:


#stateDict


# In[ ]:


def longState(search_value):
    for key, val in stateDict.items():
        if key == search_value:
            return val


# In[ ]:


fullStateName = []
for i in renamedState:
    fullStateName.append((longState(i)).capitalize())
fullStateName[:5]


# In[ ]:


def upperTwo(string):
    if string.isspace():
        return True
    else:
        return False
    


# In[ ]:


def capitalTwo(check):
    holder = []
    i = 0
    while i < len(check):
        if upperTwo(check[i]):
            holder.append(' ')
            holder.append(check[i+1].capitalize())
            i += 1
        elif upperTwo(check[i-1]):
            i += 1
            continue
        else:
            holder.append(check[i])
            i += 1
    return ''.join(holder)


# In[ ]:


upperState = []
for i in fullStateName:
    upperState.append(capitalTwo(i))


# In[ ]:


#upperState


# In[ ]:


Total_Raised = []
for i in contributions_2014['Total Raised']:
    Total_Raised.append(int(i[1:]))


# In[ ]:


contributions_2014['Total_Raised'] = Total_Raised
contributions_2014['State_Abbrv'] = renamedState
contributions_2014['State'] = upperState
contributions_2014['Party'] = party
contributions_2014['Party_Name'] = fullPartyName
contributions_2014['Full_Name'] = cleanedName
contributions_2014['First_Name'] = firstName
contributions_2014['Last_Name'] = lastName


# In[ ]:


contributions_2014 = contributions_2014.drop(['Representative', 'Office Running For', 'Total Raised'], axis = 1)


# In[ ]:


contributions_2014 = contributions_2014[['First_Name', 'Last_Name', 'State', 'Party_Name', 'Total_Raised', 'Full_Name', 'State_Abbrv', 'Party',]]


# In[ ]:


contributions_2014['Full_Name'][1] = 'Mitch McConnell'
contributions_2014['Full_Name'][10] = 'John McCain'
contributions_2014['Full_Name'][11] = 'Claire McCaskill'


# In[ ]:


contributions_2014= contributions_2014.sort_values('Last_Name').reset_index()
contributions_2014 = contributions_2014.drop(['index'], axis = 1)
contributions_2014


# In[ ]:


contributions_2014.to_csv('contributions_2014.csv', index=False)


# In[ ]:


get_ipython().system('jupyter nbconvert --to python campaignContribution2014.ipynb')


# In[ ]:





# In[ ]:




