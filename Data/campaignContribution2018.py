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


contributions_2018 = pd.read_csv('campaign_contribution_2018.csv')
stateName = pd.read_csv('stateAbbrv.csv')


# In[3]:


contributions_2018.head(5)


# In[4]:


#Finding indexes of Names that will give errors
i = 0
while i < len(contributions_2018['Representative']):
    if 'Connell' in contributions_2018['Representative'][i]:
        z = contributions_2018['Representative'][i]
        print(f'{i} = connell, {z}')
        i += 1
    elif 'Capito' in contributions_2018['Representative'][i]:
        z = contributions_2018['Representative'][i]
        print(f'{i} = capito, {z}')
        i += 1
    elif 'Sanders' in contributions_2018['Representative'][i]:
        z = contributions_2018['Representative'][i]
        print(f'{i} = sanders, {z}')
        i += 1
    elif 'Mc' in contributions_2018['Representative'][i]:
        z = contributions_2018['Representative'][i]
        print(f'{i} = Mc, {z}')
        i += 1
    elif 'Cortez' in contributions_2018['Representative'][i]:
        z = contributions_2018['Representative'][i]
        print(f'{i} = Cortez, {z}')
        i += 1
    elif 'Cindy' in contributions_2018['Representative'][i]:
        z = contributions_2018['Representative'][i]
        print(f'{i} = Cindy, {z}')
        i += 1
    elif 'Van' in contributions_2018['Representative'][i]:
        z = contributions_2018['Representative'][i]
        print(f'{i} = Van, {z}')
        i += 1
    else:
        i+= 1


# In[5]:


contributions_2018['Representative'][66] = 'CapitoShelleyMoore Capito (R-WVa)'
contributions_2018['Representative'][84] = 'HydeCindy Hyde-Smith (R-Miss)*'
contributions_2018['Representative'][15] = 'MastoCatherineCortez Masto (D-Nev)'
contributions_2018['Representative'][45] = 'HollenChrisVan Hollen (D-Md)'


# In[6]:


len(contributions_2018)


# In[7]:


stripList = contributions_2018['Representative']
namesNoAstrick = []
for i in stripList:
    namesNoAstrick.append(i[:-1])


# In[8]:


len(namesNoAstrick)


# In[9]:


# counter =0
# while counter < len(namesNoAstrick):
#     if "N00009975&cycle=2016" in namesNoAstrick[counter]:
#         print(counter)
#     else:
#         counter += 1


# In[10]:


namesNoAstrick[51]


# In[11]:


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


# In[12]:


listName = stripNames(namesNoAstrick)


# In[13]:


len(listName[0])


# In[14]:


def cleanName(string):
    i = 1
    while i < len(string):
        if string[i] >= 'A' and string[i] <= 'Z':
            #print(i)
            return string[i:]
        else:
            i+= 1


# In[15]:


#listName[1]


# In[16]:


cleanedName = []
for i in listName[0]:
    cleanedName.append(cleanName(i))
#cleanedName


# In[17]:


cleanedName[1] = 'Clair McCaskill'
cleanedName[9] = 'Mitch McConnell'


# In[18]:


splitName = []
for i in cleanedName:
    splitName.append(i.split())
Namelist = []
noMiddle =[]
for i in cleanedName:
    Namelist.append(i.split(' '))
len(Namelist)
#Namelist


# In[19]:


noMiddle = []
counter = 0
for i in Namelist:
    for j in i:
        if len(j) > 1:
            noMiddle.append(j)
            #print(f'Greater than 1 {j}')
            counter += 1
        elif len(j) <= 2:
            #print(f'Checking {j}')
            counter += 1
            continue
#             query = input('Keep this value, Y/N?')
#             if query == 'Y':
#                 noMiddle.append(j)
#                 counter += 1
#             else:
#                 continue
#                 counter += 1
        else:
            print(f'{j}')
            counter += 1
print(len(noMiddle))
firstName = noMiddle[:len(noMiddle)+1:2]
lastName = noMiddle[1:len(noMiddle)+1:2]
print(len(lastName))
print(len(firstName))
print(len(cleanedName))


# In[20]:


# for i in noMiddle:
#     print(i)
#     time.sleep(.50)


# In[21]:


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


# In[22]:


matchList = listName[1]
#matchList


# In[23]:


AP = []
for i in stateName['Abbrev']:
    if i[-1] == '.':
        AP.append(i[:-1])
    else:
        AP.append(i)


# In[24]:


stateName['AP'] = AP


# In[25]:


abbrev = stateName['AP']
abbrev = abbrev.tolist()
#abbrev
fullState = (stateName['State']).tolist()
shortAbbrev = (stateName['Code']).tolist()
fullStateLower = []
for i in fullState:
    fullStateLower.append(i.lower())
stateDict = dict(zip(shortAbbrev, fullStateLower))


# In[26]:


otherDict = dict(zip(AP, fullStateLower))
stateName['lower'] = fullStateLower


# In[27]:


len(matchList)#[95:]


# In[28]:


#stateDict


# In[29]:


#Matches the strings that have AP style abbreviation with full statenames
def getMatch(string):
    for key, value in otherDict.items():
        if value.startswith(string):
            return value


# In[30]:


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


# In[31]:


#Matches the full state names to abbreviations
def getMatch2(string):
    for key, value in stateDict.items():
        if value.startswith(string):
            return key


# In[32]:


#Calling getMatch2 with holder from getMatch
renamedState = []
for i in holder:
    if len(i) == 2:
        renamedState.append(i)
    else:
        renamedState.append(getMatch2(i))


# In[33]:


len(renamedState)


# In[34]:


contributions_2018['Representative'][45]


# In[35]:


#print(type(renamedState[45]))
renamedState[45] = 'MD'


# In[36]:


def longState(search_value):
    for key, val in stateDict.items():
        if key == search_value:
            return val


# In[37]:


fullStateName = []
for i in renamedState:
    fullStateName.append((longState(i)).capitalize())
#fullStateName


# In[38]:


def upperTwo(string):
    if string.isspace():
        return True
    else:
        return False


# In[39]:


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


# In[40]:


upperState = []
for i in fullStateName:
    upperState.append(capitalTwo(i))


# In[41]:


Total_Raised = []
for i in contributions_2018['Total Raised']:
    Total_Raised.append(int(i[1:]))


# In[42]:


len(Total_Raised)


# In[43]:


contributions_2018['Total_Raised'] = Total_Raised
contributions_2018['State_Abbrv'] = renamedState
contributions_2018['State'] = upperState
contributions_2018['Party'] = party
contributions_2018['Party_Name'] = fullPartyName
contributions_2018['Full_Name'] = cleanedName
contributions_2018['First_Name'] = firstName
contributions_2018['Last_Name'] = lastName


# In[44]:


contributions_2018 = contributions_2018.drop(['Representative', 'Office Running For', 'Total Raised'], axis = 1)


# In[45]:


contributions_2018 = contributions_2018[['First_Name', 'Last_Name', 'State', 'Party_Name', 'Total_Raised', 'Full_Name', 'State_Abbrv', 'Party']]


# In[46]:


# contributions_2018['Name'][1] = 'Claire McCaskill'
# contributions_2018['Name'][9] = 'Mitch McConnell'
# contributions_2018['Name'][84] = 'Cindy Hyde-Smith'


# In[48]:


#contributions_2018['Full_Name'][1]# = 'Claire McCaskill'
contributions_2018[Full_Name'][9] # = 'Mitch McConnell'
#contributions_2018['Name'][84]# = 'Cindy Hyde-Smith'


# In[ ]:


contributions_2018 = contributions_2018.sort_values('Last_Name').reset_index()
contributions_2018 = contributions_2018.drop(['index'], axis = 1)
contributions_2018.head()


# In[ ]:


contributions_2018.to_csv('contributions_2018.csv', index = False)


# In[ ]:


#exporting notebook to python file
get_ipython().system('jupyter nbconvert --to python campaignContribution2018.ipynb')


# In[ ]:




