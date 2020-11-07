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


#contributions_2016.head(50)


# In[4]:


contributions_2016['Representative'][2] = "ConnellMitch McConnell (R-Ky)"
contributions_2016['Representative'][52] = 'NameNone None (I-SC)'
contributions_2016['Representative'][65] = 'CapitoShelleyMoore Capito (R-WVa)'


# In[5]:


i = 0
while i < len(contributions_2016['Representative']):
    if 'Capito' in contributions_2016['Representative'][i]:
        value = contributions_2016['Representative'][i]
        print(f'Index = {i}, value is:: {value}')
        i += 1
    else:
        i += 1


# In[6]:


stripList = contributions_2016['Representative']
namesNoAstrick = []
for i in stripList:
    namesNoAstrick.append(i[:-1])


# In[7]:


#len(namesNoAstrick)


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


contributions_2016['Representative'][26]


# In[13]:


namesNoAstrick[26] = 'John McCain (R-Ariz)'
namesNoAstrick[10] = 'Claire McCaskill (D-Mo)'


# In[14]:


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


# In[15]:


listName = stripNames(namesNoAstrick)


# In[16]:


#len(listName[0])


# In[17]:


def cleanName(string):
    i = 1
    while i < len(string):
        if string[i] >= 'A' and string[i] <= 'Z':
            #print(string[i])
            return string[i:]
        else:
            i+= 1


# In[18]:


#listName[1]


# In[19]:


cleanedName = []
for i in listName[0]:
    cleanedName.append(cleanName(i))
    #print(f'{i}')
    #time.sleep(0.50)
#cleanedName


# In[20]:


print(cleanedName[26])
print(cleanedName[10])


# In[21]:


cleanedName[26] = 'John McCain'
cleanedName[10] = 'Claire McCaskill'


# In[22]:


cleanedName[65]


# In[23]:


splitName = []
for i in cleanedName:
    splitName.append(i.split())


# In[24]:


#len(cleanedName)
#cleanedName


# In[25]:


Namelist = []
noMiddle =[]
for i in cleanedName:
    Namelist.append(i.split(' '))
len(Namelist)


# In[26]:


# for i in Namelist:
#     print(f'{i}')
#     time.sleep(.50)


# In[27]:


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


# In[28]:


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


# In[29]:


matchList = listName[1]
#matchList


# In[30]:


AP = []
for i in stateName['Abbrev']:
    if i[-1] == '.':
        AP.append(i[:-1])
    else:
        AP.append(i)


# In[31]:


stateName['AP'] = AP


# In[32]:


abbrev = stateName['AP']
abbrev = abbrev.tolist()
#abbrev
fullState = (stateName['State']).tolist()
shortAbbrev = (stateName['Code']).tolist()
fullStateLower = []
for i in fullState:
    fullStateLower.append(i.lower())
stateDict = dict(zip(shortAbbrev, fullStateLower))


# In[33]:


otherDict = dict(zip(AP, fullStateLower))
stateName['lower'] = fullStateLower


# In[34]:


#len(matchList)#[95:]


# In[35]:


#stateDict


# In[36]:


#Matches the strings that have AP style abbreviation with full statenames
def getMatch(string):
    for key, value in otherDict.items():
        if value.startswith(string):
            return value


# In[37]:


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


# In[38]:


#Matches the full state names to abbreviations
def getMatch2(string):
    for key, value in stateDict.items():
        if value.startswith(string):
            return key


# In[39]:


#Calling getMatch2 with holder from getMatch
renamedState = []
for i in holder:
    if len(i) == 2:
        renamedState.append(i)
    else:
        renamedState.append(getMatch2(i))


# In[40]:


#renamedState


# In[41]:


renamedState[52] = 'SC'
renamedState[2] = 'KY'


# In[42]:


def longState(search_value):
    for key, val in stateDict.items():
        if key == search_value:
            return val


# In[43]:


fullStateName = []
for i in renamedState:
    fullStateName.append((longState(i)).capitalize())
#fullStateName


# In[44]:


def upperTwo(string):
    if string.isspace():
        return True
    else:
        return False


# In[45]:


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


# In[46]:


upperState = []
for i in fullStateName:
    upperState.append(capitalTwo(i))


# In[47]:


contributions_2016.head()


# In[48]:


Total_Raised = []
for i in contributions_2016['Total Raised']:
    Total_Raised.append(int(i[1:]))


# In[49]:


#len(Total_Raised)


# In[50]:


contributions_2016['Total_Raised'] = Total_Raised
contributions_2016['State_Abbrv'] = renamedState
contributions_2016['State'] = upperState
contributions_2016['Party'] = party
contributions_2016['Party_Name'] = fullPartyName
contributions_2016['Full_Name'] = cleanedName
contributions_2016['First_Name'] = firstName
contributions_2016['Last_Name'] = lastName


# In[51]:


#contributions_2016


# In[52]:


contributions_2016 = contributions_2016.drop(['Representative', 'Office Running For', 'Total Raised'], axis = 1)


# In[53]:


contributions_2016 = contributions_2016[['First_Name', 'Last_Name', 'State', 'Party_Name', 'Total_Raised', 'Full_Name', 'State_Abbrv', 'Party']]


# In[54]:


contributions_2016 = contributions_2016.sort_values('Last_Name').reset_index()
contributions_2016 = contributions_2016.drop(['index']
contributions_2016.head()


# In[55]:


contributions_2016.to_csv('contributions_2016.csv', index = False)


# In[56]:


get_ipython().system('jupyter nbconvert --to python campaignContribution2016.ipynb')


# In[ ]:





# In[ ]:




