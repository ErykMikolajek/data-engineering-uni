#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

df = pd.read_csv('proj2_data.csv', sep=';|\|', decimal=",")


# In[2]:


import pickle
with open('proj2_ex01.pkl', 'wb') as df_pickle:
    pickle.dump(df, df_pickle)


# In[3]:


grades = pd.read_csv('proj2_scale.txt', header=None)
grades.index = grades.index + 1
grades = grades.to_dict()[0]


# In[4]:


inv_grades = {v: k for k, v in grades.items()}
inv_grades


# In[5]:


df_scaled = df.copy()


# In[6]:


df_scaled['task_grade'].replace(inv_grades, inplace=True)
df_scaled['final_grade'].replace(inv_grades, inplace=True)


# In[7]:


with open('proj2_ex02.pkl', 'wb') as df_scaled_pickle:
    pickle.dump(df_scaled, df_scaled_pickle)


# In[8]:


df_categories = df.copy()


# In[9]:


with open('proj2_scale.txt', 'r') as scale:
    categories_list = [line.rstrip() for line in scale]


# In[10]:


df_categories['task_grade'] = df_categories['task_grade'].astype('category')
df_categories['final_grade'] = df_categories['final_grade'].astype('category')
df_categories['task_grade'] = df_categories['task_grade'].cat.set_categories(categories_list)
df_categories['final_grade'] = df_categories['final_grade'].cat.set_categories(categories_list)


# In[11]:


with open('proj2_ex03.pkl', 'wb') as df_categories_pickle:
    pickle.dump(df_categories, df_categories_pickle)


# In[12]:


num_extraction = df.copy()
num_extraction.select_dtypes(include='object')


# In[20]:


num_extraction_series = num_extraction['jury_score'].str.extract(r"(-?\d+[,\.]?\d*)").unstack()


# In[23]:


num_extraction_series_df = pd.DataFrame(num_extraction_series)
num_extraction_series_df = num_extraction_series_df.reset_index().drop(columns=['level_0', 'level_1'])
num_extraction_series_df.rename(columns={0: 'jury_score'}, inplace=True)
num_extraction_series_df['jury_score'] = num_extraction_series_df['jury_score'].str.replace(',','.')
num_extraction_series_df = num_extraction_series_df.astype(float)
num_extraction_series_df


# In[15]:


with open('proj2_ex04.pkl', 'wb') as df_extraction_pickle:
    pickle.dump(num_extraction_series_df, df_extraction_pickle)


# In[16]:


df_field = pd.get_dummies(df['field'])
df_language = pd.get_dummies(df['language'])


# In[17]:


with open('proj2_ex05_1.pkl', 'wb') as df_one_hot_field_pickle:
    pickle.dump(df_field, df_one_hot_field_pickle)


# In[18]:


with open('proj2_ex05_2.pkl', 'wb') as df_one_hot_language_pickle:
    pickle.dump(df_language, df_one_hot_language_pickle)

