#!/usr/bin/env python
# coding: utf-8

# In[4]:



import requests
from bs4 import BeautifulSoup as sc
import pandas as pd
STOCK  = {} # storing STOCK info
header_elem = [] # for table header like S.N. , Traded Companies , Max price , Min Price ...

def scrape_stock(link):
    global STOCK , header_elem
    page = requests.get(link)
    soup = sc(page.content,"html.parser")
    table = soup.find('table',{'class':'table table-condensed table-hover'}) #find table tag with class given 
    if len(header_elem) == 0: # First Time getting the Head {'SN. , 'Trade Companies', etc ...}
        table_header = table.find('tr',{'class': 'unique'}) 
        for td in table_header.find_all('td'):
            header = td.text.replace('\n','')
            STOCK[header] = []
            header_elem.append(header)
    
    table_data = table.find_all('tr')
    table_data = table_data[1:21] # only 20 data per index thus get <tr> from 0 to 19
    table_data = [data.find_all('td') for data in table_data]
    
    for td in table_data:
        for header,x in zip(STOCK.keys(),td):
            if header not in ('Traded Companies','S.N.'):
                STOCK[header].append(float(x.text))
            else:
                if header == 'S.N.':
                    try:
                        STOCK[header].append(int(x.text))
                    except:
                        break
                else:
                    STOCK[header].append(x.text)
    
index = 12 # total of 12 index

# main program starts
for i in range(0,index+1):
    link = f"http://nepalstock.com/main/todays_price/index/{i}"
    scrape_stock(link)
STOCK


# In[6]:


df = pd.DataFrame(STOCK)
df.to_csv('stock_data.csv',index =False)
df


# In[20]:


import pandas as pd
import plotly.express as px
df = pd.DataFrame(STOCK)
fig = px.box(df, x="Traded Companies", y="No. Of Transaction")
fig.show()


# In[15]:





# In[ ]:




