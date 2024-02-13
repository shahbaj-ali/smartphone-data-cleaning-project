#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df = pd.read_csv('smartphones - smartphones.csv')


# In[3]:


df.head()


# In[4]:


# cleaning the price column
# there are three problems with this column - rupee symbol, comma, and the data type is string
# lets do them one by one but before doing anything make the copy of your datafrome

df1 = df.copy()


# In[9]:


df1['price'] = df1['price'].str.replace('₹', '').str.replace(',', '').astype('int')


# In[12]:


# changing the index as per the sheet in which data is present

df1 = df1.reset_index()


# In[14]:


df1['index'] = df1['index'] + 2


# In[15]:


# now we have the index as per the data sheet (excel) 
df1


# In[16]:


# creating the set of the indexes in which there are problems

processor_rows = set((642,647,649,659,667,701,750,759,819,859,883,884,919,927,929,932,1002))
memory_rows = set((441,485,534,553,584,610,613,642,647,649,659,667,701,750,759,819,859,884,919,927,929,932,990,1002))
battery_rows = set((113,151,309,365,378,441,450,553,584,610,613,630,642,647,649,659,667,701,750,756,759,764,819,855,859,884,915,916,927,929,932,990,1002))
display_rows = set((378,441,450,553,584,610,613,630,642,647,649,659,667,701,750,759,764,819,859,884,915,916,927,929,932,990,1002))
camera_rows = set((100,113,151,157,161,238,273,308,309,323,324,365,367,378,394,441,450,484,506,534,553,571,572,575,584,610,613,615,630,642,647,649,659,667,684,687,705,711,723,728,750,756,759,764,792,819,846,854,855,858,883,884,896,915,916,927,929,932,945,956,990,995,1002,1016))


# In[21]:


df1[df1['index'].isin(processor_rows | memory_rows | battery_rows | display_rows | camera_rows)]


# In[24]:


df1[df1['index'].isin(processor_rows & memory_rows & battery_rows & display_rows & camera_rows)]['price'].mean()


# In[29]:


# we identified that most the phones in which there are some problems are not smartphone
# and we got the know by the price, phones which are less than 3000 are feature phones

df1 = df1[df1['price']>=3400]


# In[30]:


df1


# In[34]:


# now we will work on processor column

df1[df1['index'].isin(processor_rows)]


# In[33]:


# we checked that these phones are not smartphones so we are removing them

df1.drop([645,857,882,925], inplace=True)


# In[39]:


# now lets work on ram column

df1[df1['index'].isin(memory_rows)]


# In[38]:


# 582 seems a feature phone, so we are droping this row.

df1.drop(582, inplace=True)


# In[54]:


# now we will work on battery column

df1[df1['index'].isin(battery_rows)]


# In[42]:


df1.drop([376, 754], inplace=True)


# In[44]:


temp_df = df1[df1['index'].isin(battery_rows)]


# In[50]:


x = temp_df.iloc[:,7:].shift(1, axis=1).values


# In[51]:


x


# In[53]:


df1.loc[temp_df.index, df1.columns[7:]] = x


# In[67]:


# now we will work on camera column
df1[df1['index'].isin(camera_rows)]
# 155 271 


# In[57]:


df1.drop([155, 271], inplace=True)


# In[59]:


temp_df = df1[df1['index'].isin(camera_rows)]


# In[65]:


temp_df = temp_df[~temp_df['camera'].str.contains('MP')]


# In[66]:


df1.loc[temp_df.index, 'camera'] = temp_df['card'].values


# In[75]:


# now we will work on card column

df1['card'].value_counts()


# In[73]:


temp_df = df1[df1['card'].str.contains('MP')]


# In[74]:


df1.loc[temp_df.index, 'card'] = 'Memory Card Not Supported'


# In[79]:


temp_df = df1[~df1['card'].str.contains('Memory Card')]


# In[81]:


df1.loc[temp_df.index, 'os'] = temp_df['card'].values


# In[82]:


df1.loc[temp_df.index, 'card'] = 'Memory Card Not Supported'


# In[84]:


df1['card'].value_counts()


# In[99]:


temp_df = df1[df1['os'].str.contains('Memory Card')]


# In[102]:


temp_df = temp_df[~temp_df['os'].str.contains('Memory Card Not Supported')]


# In[103]:


df1.head(2)


# In[104]:


df1.loc[temp_df.index, 'card'] = temp_df['os'].values


# In[105]:


df1[df1['os'].str.contains('Memory Card')]


# In[107]:


temp_df = df1[df1['os'].str.contains('Memory Card')]


# In[112]:


temp_df = df1[df1['os'] == 'Bluetooth']


# In[113]:


df1.loc[temp_df.index, 'os'] = np.nan


# In[114]:


df1['os'].value_counts()


# In[121]:


df1.head(2)


# In[119]:


pd.set_option('display.max_rows', None)


# In[127]:


df1['os'].value_counts()

