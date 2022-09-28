#!/usr/bin/env python
# coding: utf-8





import requests
from bs4 import BeautifulSoup as sc
import pandas as pd
STOCK  = {} # storing STOCK info
header_elem = [] 

def scrape_stock(link):
    global STOCK , header_elem
    page = requests.get(link)
    soup = sc(page.content,"html.parser")
    table = soup.find('table',{'class':'table table-condensed table-hover'}) 
    if len(header_elem) == 0:
        table_header = table.find('tr',{'class': 'unique'}) 
        for td in table_header.find_all('td'):
            header = td.text.replace('\n','')
            STOCK[header] = []
            header_elem.append(header)
    
    table_data = table.find_all('tr')
    table_data = table_data[1:21] 
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
    
index = 12 
for i in range(0,index+1):
    link = f"http://nepalstock.com/main/todays_price/index/{i}"
    scrape_stock(link)
STOCK



# Creating and reading CSV file
df = pd.DataFrame(STOCK)
df.to_csv('stock_data.csv',index =False)
df


# Visualization 
import pandas as pd
import plotly.express as px
df = pd.DataFrame(STOCK)
fig = px.box(df, x="Traded Companies", y="No. Of Transaction")
fig.show()













