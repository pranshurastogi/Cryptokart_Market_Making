#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Date 12.march.2019
# By - Pranshu Rastogi
# Market making strategy

# Importing libraries
import requests
import random
import json
import time
from binance.client import Client
from binance.enums import *
# Binance API KEY and SECRET KEY PLEASE INSERT HERE


# In[2]:


# Variable Declaration 
client = Client("API KEY","SECRET KEY")
Bitmex_Pair = 'XBTUSD'                                            #Used in Url_Bitmex,change to get different crypto pair
client_id = "Cryptokart Api key USER 2"                 # For user Authentication purpose
client_secret= "Cryptokart Secret Key user 2"              #For user authentication purpose
market_name = "BTCUSDT"


# In[3]:


# Taking Market Price from Bitmex

# Gateway_Bitmex = "https://www.bitmex.com/api/v1/"
# Url_Bitmex = Gateway_Bitmex + "trade?symbol="+Bitmex_Pair+"&count=1&reverse=true"
# r = requests.get(Url_Bitmex)
# Market_Price_Bitmex = (r.json())[0]['price']
# print(Market_Price_Bitmex)


prices = client.get_all_tickers()
if(prices[11]['symbol']== 'BTCUSDT'):
    Market_Price_Bitmex = float(prices[11]['price'])
    print(Market_Price_Bitmex)


# In[4]:


# Function to fire a single order
# Note = Side == 1 is "Sell" and Side == 2 is "Buy"
#Note = Beside Side everything else is in string

def FireOrder_Market(client_id,client_secret,market_name,side,amount):
    url ="https://cryptokart.io:1337/matchengine/order/putMarket"
    payload=({"client_id":client_id,"client_secret": client_secret,"market_name": market_name,"side": side,"amount": amount})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)

def Market_status_Today(client_id,client_secret,market_name):
    url ="https://cryptokart.io:1337/matchengine/market/statusToday"
    payload=({"client_id":client_id,"client_secret": client_secret,"market_name": market_name})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)
Market_status_Today(client_id,client_secret,market_name)
    

def CancelAllOrders(client_id,client_secret):
    url = "https://cryptokart.io:1337/matchengine/order/cancelAll"
    payload=({"client_id":client_id,"client_secret": client_secret})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)


# In[ ]:


def Trade_Order_Market():
    while(True):
        try:
            random_qty_int = random.uniform(5,20)
            random_qty = str(round((random_qty_int/400),3))
            random_buy_sell = random.randint(1,2)
            if(random_buy_sell == 1):
                random_qty_int = random.uniform(5,20)
                random_qty = str(round((random_qty_int/400),3))
                random_time = random.randint(15,30)
                FireOrder_Market(client_id,client_secret,"BTCUSDT",1,random_qty)
                time.sleep(random_time)
                random_time = random.randint(250,390)
                FireOrder_Market(client_id,client_secret,"BTCUSDT",2,random_qty)
                time.sleep(random_time)
            elif(random_buy_sell == 2):
                random_qty_int = random.uniform(5,20)
                random_qty = str(round((random_qty_int/400),3))
                random_time = random.randint(15,30)
                FireOrder_Market(client_id,client_secret,"BTCUSDT",2,random_qty)
                time.sleep(random_time)
                random_time = random.randint(250,390)
                FireOrder_Market(client_id,client_secret,"BTCUSDT",1,random_qty)
                time.sleep(random_time)
            else:
                print("This can't happen, Your code is playing with you...")
                

            
        except:
            continue
Trade_Order_Market()



