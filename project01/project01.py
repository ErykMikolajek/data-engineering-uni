#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
df = pd.read_csv('lab1_ex01.csv')


# In[2]:


import numpy as np
#df['First column'] = pd.to_numeric(df['First column'], errors='coerce')
#df['two'] = pd.to_numeric(df['two'], errors='coerce')
#df['three'] = pd.to_numeric(df['three'], errors='coerce')
d = []
for (col_name, serie) in df.items():
    type_out = 'int' if serie.dtype == 'int64' else ('float' if serie.dtype == 'float64' else 'other')
    d.append([col_name, serie.isnull().sum()/serie.size, type_out])


# In[3]:


json_df = pd.DataFrame(d, columns=['name', 'missing', 'type'])


# In[4]:


json_dump = json_df.to_json('ex01_fields.json', orient = 'records', indent=4)


# In[5]:


d2 = {}
for (col_name, serie) in df.items():
    d2[col_name] = serie.describe()

json2_df = pd.DataFrame(d2)


# In[6]:


json2_df.to_json('ex02_stats.json', orient = 'columns', indent=4)


# In[7]:


import re
columns_names = []
for column_name in df.columns:
    column_name = re.sub('[^A-Za-z0-9_ ]', '', column_name)
    column_name = column_name.lower()
    #column_name = re.sub(' $', '', column_name)
    column_name = re.sub('[ ]', '_', column_name)
    columns_names.append(column_name)
df.columns = columns_names

df.to_csv('ex03_columns.csv', index=False)


# In[8]:


df.to_excel('ex04_excel.xlsx', index=False)


# In[9]:


df.to_json('ex04_json.json', orient = 'records', indent=4)


# In[11]:


import pickle
with open('ex04_pickle.pkl', 'wb') as pickle_file:
    pickle.dump(df, pickle_file)


# In[12]:


unpickled_df = pd.read_pickle('lab1_ex05.pkl')


# In[36]:


to_markdown_columns = unpickled_df.iloc[:, [1, 2]]
to_markdown_columns = to_markdown_columns.fillna('')
to_markdown_columns = to_markdown_columns[to_markdown_columns.index.str.startswith('v')]
to_markdown_columns.to_markdown('ex05_table.md')

# In[43]:


import json
with open('lab1_ex06.json') as json_data:
    json_to_normalize = json.load(json_data)
json_to_normalize_df = pd.json_normalize(json_to_normalize)


# In[44]:


with open('ex06_pickle.pkl', 'wb') as pickle_json:
    pickle.dump(json_to_normalize_df, pickle_json)

