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
client = Client("Binance API KEY","Binance API secret key")


# In[2]:


# Variable Declaration 

# Bitmex_Pair = 'XBTUSD'                                            #Used in Url_Bitmex,change to get different crypto pair
client_id = "Cryptokart APi Key"                                    # For user Authentication purpose
client_secret= "Cryptokart Secret Key"                               #For user authentication purpose
price_regulator = 150
market_name = "BTCUSDT"
user_id = 56


# In[3]:

#---------------------------------Previous code to take price from Bitmex----------------------------#
# Taking Market Price from Bitmex
# Gateway_Bitmex = "https://www.bitmex.com/api/v1/"
# Url_Bitmex = Gateway_Bitmex + "trade?symbol="+Bitmex_Pair+"&count=1&reverse=true"
# r = requests.get(Url_Bitmex)
# Market_Price_Bitmex = (r.json())[0]['price']
#------------------------------------------------------------------------------------------------------


prices = client.get_all_tickers()
if(prices[11]['symbol']== 'BTCUSDT'):
    Market_Price_Bitmex = float(prices[11]['price'])
    print(Market_Price_Bitmex)


# In[4]:


# Function to fire a single order
# Note = Side == 1 is "Sell" and Side == 2 is "Buy"
#Note = Beside Side everything else is in string

def FireOrder_Limit(client_id,client_secret,market_name,side,amount,price):
    url = "https://cryptokart.io:1337/matchengine/order/putLimit"
    payload=({"client_id":client_id,"client_secret": client_secret,"market_name": market_name,"side": side,"amount": amount,"price": price})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)

def CancelAllOrders(client_id,client_secret):
    url = "https://cryptokart.io:1337/matchengine/order/cancelAll"
    payload=({"client_id":client_id,"client_secret": client_secret})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)
    print("sarre order cancel hogye")
    
def Pending_Orders_User(client_id,client_secret,market_name,user_id):
    url = "https://cryptokart.io:1337/matchengine/order/pending"

    payload = ({"client_id" :client_id,
    "client_secret":client_secret,
        "market_name" :market_name,
        "offset" : 0,
        "limit" : 100,
        "user_id": user_id
    })
    
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
        }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    No_of_orders = (len(response.json()['result']['records']))
    random_order_number = (random.randint(0,No_of_orders))-1 
    random_order_id = ((response.json()['result']['records'][random_order_number]['id']))
    print(random_order_id)
    return random_order_id,No_of_orders

def Cancel_Order(client_id,client_secret,market_name,order_id):
    url = "https://cryptokart.io:1337/matchengine/order/cancel"

    payload = ({"client_id" :client_id,
    "client_secret":  client_secret,"market_name" : market_name,"order_id" : order_id
    })
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    print(response.text,"Order cancel hogya")
    

# FireOrder_Limit(client_id,client_secret,"BTCUSDT",1,"0.062","4298")


# In[ ]:


def Bulk_Buy_Order(No_of_Orders,arg1_qty_int,arg2_qty_int,arg1_Price_int,arg2_Price_int,market_name):
    for i in range(No_of_Orders):
        random_qty_int = random.uniform(arg1_qty_int,arg2_qty_int)
        random_qty = str(round((random_qty_int/400),3))
        random_price = round((random.uniform(arg1_Price_int,arg2_Price_int)),2)
        random_price_str = str(random_price)
        Order_placement = FireOrder_Limit(client_id,client_secret,market_name,2,random_qty,random_price_str)
        
def Bulk_Sell_Order(No_of_Orders,arg1_qty_int,arg2_qty_int,arg1_Price_int,arg2_Price_int,market_name):
    for i in range(No_of_Orders):
        random_qty_int = random.uniform(arg1_qty_int,arg2_qty_int)
        random_qty = str(round((random_qty_int/400),3))
        random_price = round((random.uniform(arg1_Price_int,arg2_Price_int)),2)
        random_price_str = str(random_price)
        Order_placement = FireOrder_Limit(client_id,client_secret,market_name,1,random_qty,random_price_str)
        
Bulk_Buy_Order(9,2,20,Market_Price_Bitmex-price_regulator,Market_Price_Bitmex,market_name)
Bulk_Sell_Order(9,2,20,Market_Price_Bitmex,Market_Price_Bitmex + price_regulator,market_name)


        


# In[ ]:


def Trade_Order_Limit():
    while(True):
        try:
            Order_len = order_id = Pending_Orders_User(client_id,client_secret,market_name,user_id)[1]
            if(Order_len >10):
                prices = client.get_all_tickers()
                if(prices[11]['symbol']== 'BTCUSDT'):
                    Market_Price_Bitmex = float(prices[11]['price'])
                    print(Market_Price_Bitmex)

                
                order_id = Pending_Orders_User(client_id,client_secret,market_name,user_id)[0]
                Cancel_Order(client_id,client_secret,market_name,order_id)
                Bulk_Buy_Order(2,2,20,Market_Price_Bitmex-price_regulator,Market_Price_Bitmex,market_name)
                time.sleep(5)
                
                order_id = Pending_Orders_User(client_id,client_secret,market_name,user_id)[0]
                Cancel_Order(client_id,client_secret,market_name,order_id)
                Bulk_Sell_Order(2,2,20,Market_Price_Bitmex,Market_Price_Bitmex + price_regulator,market_name)
                time.sleep(5)
            else:
                Bulk_Buy_Order(5,2,20,Market_Price_Bitmex-price_regulator,Market_Price_Bitmex,market_name)
                Bulk_Sell_Order(5,2,20,Market_Price_Bitmex,Market_Price_Bitmex + price_regulator,market_name)

        except KeyboardInterrupt:
#             CancelAllOrders(client_id,client_secret)
            print ("May the force with you")
            sys.exit()
        except Exception as e:
#             CancelAllOrders(client_id,client_secret)
            print("EXception aaya Bhaggoooo !!!!!!! \n \n \n")
            print(e)
            continue
Trade_Order_Limit()





