#!/usr/bin/env python
# coding: utf-8

# In[65]:


import pandas as pd


# In[66]:


import psycopg2

from sqlalchemy import create_engine ## sqlalchemy가 있는이유는 엔진을 만들기 위해서


# In[67]:


indata =     pd.read_csv("../dataset/kopo_decision_tree_all_new.csv")


# In[68]:


indata.shape ## 총 몇 행과 컬럼이 있는지를 확인하는 것


# In[69]:


indata.columns ## 어떤 컬럼들이 있는지 확인하기


# In[70]:


indata.columns.str.lower() ## 문자열 컬럼들을 스트링으로 바꿔준 이후 소문자로 변경하기


# In[71]:


# 3. 데이터처리(컬럼 소문자로 변환)


# In[72]:


indata.columns = indata.columns.str.lower() ## DB저장 전에 한번에 컬럼을 소문자로 바꿔주기


# In[ ]:





# In[ ]:


# 4. 데이터저장하기


# In[89]:


targetDbIp = "192.168.110.111"
taergetDbPort = "5432"
targetDbId = "kopo"
targetDbPw = "kopo"
targetDbName = "kopodb"


# In[90]:


targetDbPrefix = "postgresql://"


# In[91]:


targetUrl = "{}{}:{}@{}:{}/{}".format(targetDbPrefix,
                                   targetDbId,
                                   targetDbPw,
                                   targetDbIp,
                                   taergetDbPort, 
                                   targetDbName)


# In[92]:


pg_kopo_engine = create_engine(targetUrl)


# In[93]:


tablename = "pg_result_EH"

try:
    indata.to_sql(name = tablename,
             con = pg_kopo_engine,
             if_exists = "replace", index = False)
    print("{} unload 성공!".format(tablename))
except Exception as e:
    print(e)


# In[94]:


indata.to_sql(name = tablename,
             con = pg_kopo_engine,
             if_exists = "replace",
             index = False)


# In[ ]:




