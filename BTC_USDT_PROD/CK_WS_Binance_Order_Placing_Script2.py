#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing required Libraries
import requests
import random
import json
import time

from binance.client import Client
from binance.enums import *


# In[2]:


#Variable Declaration

timestamp = (round(time.time()/1000))
client_id = "enter client id"                     # Cryptokart iser client id
client_secret= "enter client secret"            # Cryptokart User Client Secret 

Binance_Api_key = "Binance API Key"                                # Binance API Key
Binance_Api_Secret = "Binance Secret key "                         # Binance Secret Key

market_name = "BTCUSDT"                                            # Market Name in which trade will occur

CK_url = "https://test.cryptokart.io:1337/"                        # Change this URL to go from Staging to Production

Admin_Url_API_Call = "http://13.127.78.141:8080"                   # This Url is with extra privilige to get user id of other user

Websocket_Url = "wss://tsocket.cryptokart.io:453"                  # Url to access Websockets

Bot_ID_Filler = 49                                                 # This is User ID of bot who is filling the order, in this case ID = 49 i.e, of Saroj@mailinator.com


# In[3]:


# Function for specific tasks

# Fun(1) -> Order_Deal Function is from postman , It will give the order deal wrt to ID

def order_deals_postman(client_id,client_secret,order_id,offset,limit):
    url = CK_url+"matchengine/order/deals"
    payload=({"client_id":client_id,"client_secret": client_secret,"order_id":order_id,"offset":offset,"limit":limit})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    a =(response.json())
#   print((a['result']['records']))
    return (a['result']['records'])

# Demo Function Call
# order_deals_postman(client_id,client_secret,931183,0,10)


# Fun(2) -> Order_Finished Function is from Postman, It will give details of all the finished orders

def order_finished_detail_postman(client_id,client_secret,order_id):
    url = CK_url+"matchengine/order/finishedDetail"
    payload=({"client_id":client_id,"client_secret": client_secret,"order_id":order_id})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    a = (response.json())
#     print(a)
    return (a['result'])   

# Demo Function Call
# order_finished_detail_postman(client_id,client_secret,931178)


# Fun(3) -> This function is provided by admin rights with some extra priviliges
# It will provide the user ID of other user who finished that particular order
# To make  any changes watch out for the url

def order_finished_extra_access(order_id):
    basic_url = Admin_Url_API_Call
    payload=({"id":1,"method":'order.finished_detail',"params":[order_id]})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", basic_url, data=json.dumps(payload), headers=headers)
    a =(response.json())
    return (a['result'])

# Demo Function call
# order_finished_extra_access(931184)


# FUN(4 , 5) -> This function will place Market Order for BUY and SELL on Binance
def Binance_Market_order_Buy(market_name,qty):
    client = Client(Binance_Api_key,Binance_Api_Secret)
    order = client.order_market_buy(symbol=market_name,quantity=qty)
    print(order)
    
def Binance_Market_order_Sell(market_name,qty):
    client = Client(Binance_Api_key,Binance_Api_Secret)
    order = client.order_market_sell(symbol=market_name,quantity=qty)
    print(order)
    


# In[ ]:


# First step to get any Data from Ws is to create connection
# Upcoming two commands will create connection with websocket
from websocket import create_connection
ws = create_connection(Websocket_Url)

# Sending Cliend ID and Client Secret to verify the credentials to access Private Data
ws.send(json.dumps({"id":1,"method":'server.sign',"params":[client_id,client_secret,timestamp]}))
result = (ws.recv())
a = (json.loads(result))
print(a)    

# This will keep on running and getting the response from websocket
while(True):
    # Order.Subscribe gives us all the details that happens when any operation happens on Orders
    b =ws.send(json.dumps({"id":1,"method":'order.subscribe',"params":["BTCUSDT"]}))
    result = (ws.recv())
    a = (json.loads(result))
    
# This if("method" in a): only executes when some execution of order take place i.e, put,update,delete

    if("method" in a):
#         print(result)

# Here 2 indicates the id when order is filled , id == 3 is when order get finished or cancelled
# And Id == 1 is when order is created
        if((a["params"][0])==2):                                                  #Check param id ==2
            id = a["params"][1]["id"]                                             # It will store the Order ID
            deal_id = order_deals_postman(client_id,client_secret,id,0,10)   
            deal_order_id = deal_id[0]['deal_order_id']                           # It will get the deal ID
            price =deal_id[0]['price']                                           
            amount = deal_id[0]['amount']
            Final_data= order_finished_extra_access(deal_order_id)               # This is will give USer ID of other user
            if(Final_data['user'] == Bot_ID_Filler):                             #  Will check whether order is filled by bot or Not 
                print("\n \n \t NOTE: ORDER IS FILLED BY OUR BOT HAVING USER ID, PRICE AND AMOUNT", Bot_ID_Filler, price , amount)
            else:
                print("\n \n NOTE: PARTIALLY FILLED -> ORDER PLACED ON BINANCE WITH PRICE AND AMOUNT",price,amount)
                 
                # Checking whether the sell order or buy
                if((Final_data['side'])==1):                                     
                    Binance_Market_order_Sell(market_name,amount)
                elif(Final_data('side')== 2):
                    Binance_Market_order_Buy(market_name,amount)
                else:
                    print("Emergency !! Call the code creator asap, because it can't print in any case")
        
        # Now checking id == 3 that means either order get FInished by fully filled or it get cancelled
        elif((a["params"][0])==3):
            id = a["params"][1]["id"]
            order_deals = order_deals_postman(client_id,client_secret,id,0,10)
            
            # checking len of order deals, because if order get cancelled without a single fill , The list should be empty
            if(len(order_deals) == 0):
                print("\n \n NOTE: ORDER GET CANCELLED WITHOUT ANY FILL , SAD IS'NT IT")
            else:
                deal_order_id = order_deals[0]['deal_order_id']
                price =order_deals[0]['price']
                amount = order_deals[0]['amount']
                res = order_finished_detail_postman(client_id,client_secret,id)
                deal_stock = res['deal_stock']
                amount_deal = res['amount']
                ftime = res['ftime']                                               # ftime = Finished Time
                time = order_deals[0]['time']
                
                # If amount and deal_stock will same then only order is finished otherwise cancelled
                if(amount_deal == deal_stock):
                    check_user = order_finished_extra_access(deal_order_id)
                    if(check_user['user'] == Bot_ID_Filler):                     # Checking whther User is bot or Real
                        print("\n \n \t NOTE : ORDER GET FINISHED BY OUR OWN BOT, FOUND THE VICTIM!!",price,amount)
                    else:
                        print("\n \n \t ORDER GET FINISHED BY SOME REAL USER, TIME TO MAKE MONEY!!",price ,amount)
                        if((check_user['side'])==1):
                            Binance_Market_order_Sell(market_name,amount)
                        elif((check_user['side'])== 2):
                            Binance_Market_order_Buy(market_name,amount)
                        else:
                            print("Emergency !! Call the code creator asap, because it can't print in any case")
                    
                else:
                    print("\n \n \t ORDER GET CANCELLED AFTER SOME FILLING HAS BEEN DONE")

                        
        else:
            print("Breathe IN Breathe  OUT.. order place hua hai bss")
                        
            
ws.close()


# In[ ]:




