#!/usr/bin/env python
# coding: utf-8

# Small code snippets go directly in the notebook

# In[1]:


def add(a, b):
    return a + b


# In[2]:


add(1, 2)


# Larger code goes into a regular Python file

# In[3]:


import os, sys
code_dir = os.path.abspath(os.path.join(os.getcwd(), 'code'))
sys.path.insert(0, code_dir)


# In[4]:


from fizzbuzz import fizz_buzz


# In[5]:


fizz_buzz(18)


# We can load our data from outside the notebook

# In[6]:


#import os
data_file = os.path.abspath(os.path.join(os.getcwd(), 'data', 'project_size.csv'))


# In[7]:


import pandas as pd
 
df = pd.read_csv(data_file, delimiter=';')


# In[8]:


df


# In[ ]:




