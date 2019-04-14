#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing required Libraries
import requests
import random
import json
import time
import sys

from binance.client import Client
from binance.enums import *


# In[2]:




#This function is provided with python-binance in order to get data you have to pass Keys here
#For more info go to this URl -> https://python-binance.readthedocs.io/en/latest/binance.html
client = Client("Binance API key","Binance Secret Key")    #No need to provide key here in this file as we are using only public data's

#Function to get Market Price from Binance
#Note change prices[11]['symbol']== 'BTCUSDT' this to get price of different markets {11,"BTCUSDT"}
def Market_Price_Binance():
    prices = client.get_all_tickers()
    if(prices[11]['symbol']== 'BTCUSDT'):                    #Change this to get different LTP for diff market
        LTP_Binance = float(prices[11]['price'])
        print("Market price of BTCUSDT -> ", LTP_Binance)
        return LTP_Binance
LTP = Market_Price_Binance()                                       #This value is used in variable Price regulator


# In[3]:



#Variable Declaration
client_id = ""    
client_secret= ""     # Provide API client secret key to access the data
price_regulator = (LTP *(.1))/100                             # Take 1% price of Market Price to regulate the spread
price_regulator2 =(LTP *(.3))/100                             # Take 3% price of Market Price to regulate the spread
market_name = "BTCUSDT"                                    # Enter the Market Name you want to trade in
user_id = 75                                              # This is id of the user whose client_ID and secret is used
CK_url = "https://test.cryptokart.io:1337/"                # Change this URL to go from Staging to Production


# In[ ]:


# Amount Generator variables
# A random integer will be taken b/w lower bound and upper bound and then it is divided with amt_minimiser
#Example for the range of LB and UB -> 2and 20 and amt_minimizer 400
# the range will be 2/400 and 20/400 -> 0.005 and 0.05[Amount will be between these two]
lower_bound_amt = 0.003
upper_bound_amt = 0.212


# Quantity Round OFF integer
Qty_RoundOff = 3

# Price Round OFF integer
Price_RoundOff = 2

#Bulk Order qty Initially
bulk_order_qty = 10

# Order qty for regular interval
reg_ord_qty = 1

# If order get sudden wiped off qty, this is replaced by more dynamic thing refer line 223
# sudd_ord_qty = 4


# Minimum order we required in a order book
min_order_length = 20

#Time Quantum for time.sleep() to delay b/w two orders
def time_quantum_delay():
    time.sleep(5)


# In[ ]:


#Functions to perform some operations

# Note = Side == 1 is "Sell" and Side == 2 is "Buy"
# Note = Beside Side everything else is in string

# Fun(1) -> FireOrderLimit this will place limit order as per the given arguments
def FireOrder_Limit(client_id,client_secret,market_name,side,amount,price):
    url = CK_url+"matchengine/order/putLimit"
    payload=({"client_id":client_id,"client_secret": client_secret,"market_name": market_name,"side": side,"amount": amount,"price": price})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)
# Demo Function Call
# FireOrder_Limit(client_id,client_secret,market_name,1,"0.03","4333")


# Fun(2) -> It will cancel all order at once
def CancelAllOrders(client_id,client_secret):
    url = CK_url+"matchengine/order/cancelAll"
    payload=({"client_id":client_id,"client_secret": client_secret})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)
    print("\n \n \t WARNING : ALL ORDERS HAS BEEN CANCELLED\n \n")
# Demo Function Call
# CancelAllOrders(client_id,client_secret)


# Fun(3) -> Pending user Details, It will give details of all the pending orders
# This function is modified to also Provide Number of orders left and generate a random Order ID

def Pending_Orders_User(client_id,client_secret,market_name,user_id):
    url = CK_url+"matchengine/order/pending"

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

    # From here the function is modified to get Number of orders and Random Order ID
    No_of_orders = (len(response.json()['result']['records']))
    random_order_number = (random.randint(0,No_of_orders))-1
    random_order_id = ((response.json()['result']['records'][random_order_number]['id']))
    print(random_order_id)
    return random_order_id,No_of_orders

# Demo Function Call
# Pending_Orders_User(client_id,client_secret,market_name,user_id)


# Fun(4) -> Cancel Order , It will cancel a order provided with orderID

def Cancel_Order(client_id,client_secret,market_name,order_id):
    url = CK_url+"matchengine/order/cancel"

    payload = ({"client_id" :client_id,
    "client_secret":  client_secret,"market_name" : market_name,"order_id" : order_id
    })
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    print(response.text,"\n \n \t WARNING : THIS ORDER HAS BEEN CANCELLED " , order_id)



# In[ ]:


# Now we have two Function to place Bulk orders of Buy and Sell

def Bulk_Buy_Order(No_of_Orders,arg1_qty_int,arg2_qty_int,arg1_Price_int,arg2_Price_int,market_name):
    for i in range(No_of_Orders):
        random_qty_int = random.uniform(arg1_qty_int,arg2_qty_int)
        random_qty = str(round((random_qty_int),Qty_RoundOff))
        random_price = round((random.uniform(arg1_Price_int,arg2_Price_int)),Price_RoundOff)
        random_price_str = str(random_price)
        Order_placement = FireOrder_Limit(client_id,client_secret,market_name,2,random_qty,random_price_str)


def Bulk_Sell_Order(No_of_Orders,arg1_qty_int,arg2_qty_int,arg1_Price_int,arg2_Price_int,market_name):
    for i in range(No_of_Orders):
        random_qty_int = random.uniform(arg1_qty_int,arg2_qty_int)
        random_qty = str(round((random_qty_int),Qty_RoundOff))
        random_price = round((random.uniform(arg1_Price_int,arg2_Price_int)),Price_RoundOff)
        random_price_str = str(random_price)
        Order_placement = FireOrder_Limit(client_id,client_secret,market_name,1,random_qty,random_price_str)



LTP = Market_Price_Binance()                                      # Will store LTP from Binance
Bulk_Buy_Order(bulk_order_qty,lower_bound_amt,upper_bound_amt,LTP-price_regulator2,LTP-price_regulator,market_name)
print("\n \n \t BULK BUY ORDERS HAS BEEN PLACED \n \n")
Bulk_Sell_Order(bulk_order_qty,lower_bound_amt,upper_bound_amt,LTP+price_regulator,LTP + price_regulator2,market_name)
print("\n \n \t BULK SELL ORDERS HAS BEEN PLACED \n \n")


# In[ ]:


# This is where Magic Happens , This function will run continously and place and cancel order accordingly

def Trade_Order_Limit():
    while(True):
        try:
            Order_len = Pending_Orders_User(client_id,client_secret,market_name,user_id)[1]
            if(Order_len > min_order_length):
                LTP = Market_Price_Binance()                          # Will store LTP from Binance

                order_id = Pending_Orders_User(client_id,client_secret,market_name,user_id)[0]    # Random Order ID generated
                Cancel_Order(client_id,client_secret,market_name,order_id)
                Bulk_Buy_Order(reg_ord_qty,lower_bound_amt,upper_bound_amt,LTP-price_regulator2,LTP-price_regulator,market_name)
                time_quantum_delay()

                order_id = Pending_Orders_User(client_id,client_secret,market_name,user_id)[0]
                Cancel_Order(client_id,client_secret,market_name,order_id)
                Bulk_Sell_Order(reg_ord_qty,lower_bound_amt,upper_bound_amt,LTP+price_regulator,LTP + price_regulator2,market_name)
                time_quantum_delay()
            else:
                print(Order_len)
                LTP = Market_Price_Binance()                          # Will store LTP from Binance
                value = min_order_length - Order_len
                value = (int(value/2)) + 1
                for i in range(value):
                        Bulk_Buy_Order(1,lower_bound_amt,upper_bound_amt,LTP-price_regulator2,LTP-price_regulator,market_name)
                        Bulk_Sell_Order(1,lower_bound_amt,upper_bound_amt,LTP+price_regulator,LTP + price_regulator2,market_name)
        except KeyboardInterrupt:
#             CancelAllOrders(client_id,client_secret)
            print ("May the force with you")
            sys.exit()
        except Exception as e:
#             CancelAllOrders(client_id,client_secret)
            print("\n \n \t \t EXCEPTION FOUND !! BE CAUTIOUS \n \n \n")
            print(e)
            continue
Trade_Order_Limit()

