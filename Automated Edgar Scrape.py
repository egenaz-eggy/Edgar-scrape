#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import selenium
from bs4 import BeautifulSoup
import time
import requests
import datetime
import unlzw3
from pathlib import Path

headers = {"user-agent": "*your name*, *Institution* *email*"}


# In[2]:


def sec_index(year, quarter):
    url = 'https://www.sec.gov/Archives/edgar/full-index/' + str(year) + '/QTR' + str(quarter) + '/xbrl.Z'
    r = requests.get(url, headers = headers, allow_redirects = True)
    open('{}_QTR{}.Z'.format(year, quarter), 'wb').write(r.content)
    uncompressed_data = str(unlzw3.unlzw(Path('{}_QTR{}.Z'.format(year, quarter)).read_bytes())).replace('\\n', '\n').split('\n')
    df = pd.DataFrame(uncompressed_data[8:9]+uncompressed_data[10:-1])
    df.columns = df.iloc[0]
    df = df[1:]
    qtr3 = pd.DataFrame(columns=['CIK', 'Company Name', 'Form Type', 'Date Filed', 'Filename'])
    qtr0 = qtr3
    qtr1 = qtr3
    qtr2 = qtr3
    qtr4 = qtr3
    qtr5 = qtr3

    for i in range(1, len(df)):
        a = df['CIK|Company Name|Form Type|Date Filed|Filename'][i].split('|')[0]
        qtr0 = qtr0.append({'CIK': a}, ignore_index=True)

        b = df['CIK|Company Name|Form Type|Date Filed|Filename'][i].split('|')[1]
        qtr1 = qtr1.append({'Company Name': b}, ignore_index=True)

        c = df['CIK|Company Name|Form Type|Date Filed|Filename'][i].split('|')[2]
        qtr2 = qtr2.append({'Form Type': c}, ignore_index=True)

        d = df['CIK|Company Name|Form Type|Date Filed|Filename'][i].split('|')[3]
        qtr4 = qtr4.append({'Date Filed': d}, ignore_index=True)

        e = df['CIK|Company Name|Form Type|Date Filed|Filename'][i].split('|')[4]
        qtr5 = qtr5.append({'Filename': e}, ignore_index=True)
        
        datanew = pd.concat([qtr0['CIK'], qtr1['Company Name'], qtr2['Form Type'], qtr4['Date Filed'], qtr5['Filename']], axis=1)
    return datanew


# In[ ]:


sec_index(2016, 1)

