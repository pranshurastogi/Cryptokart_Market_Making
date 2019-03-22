#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import time
import requests
from binance.client import Client


# In[2]:


timestamp = (round(time.time()/1000))
client_id = "Cryptokart Api key User 1"                 # For user Authentication purpose
client_secret= "Cryptokart Secret key User 1"              #For user authentication purpose

Binance_Api_key = "Binance API Key"
Binance_Api_Secret = "Binance Secret key "

market_name = "BTCUSDT"


# In[3]:


def order_deals_postman(client_id,client_secret,order_id,offset,limit):
    url = "https://cryptokart.io:1337/matchengine/order/deals"
    payload=({"client_id":client_id,"client_secret": client_secret,"order_id":order_id,"offset":offset,"limit":limit})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    a =(response.json())
#     print((a['result']['records']))
    return (a['result']['records'])
# b = order_deals_postman(client_id,client_secret,931183,0,10)
# print(b)

def order_finished_detail_postman(client_id,client_secret,order_id):
    url = "https://cryptokart.io:1337/matchengine/order/finishedDetail"
    payload=({"client_id":client_id,"client_secret": client_secret,"order_id":order_id})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    a = (response.json())
    print(a)
    return (a['result'])          
b =order_finished_detail_postman(client_id,client_secret,931178)
print(b)

def order_finished_extra_access(order_id):
    basic_url = "http://13.127.78.141:8080"
    payload=({"id":1,"method":'order.finished_detail',"params":[order_id]})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", basic_url, data=json.dumps(payload), headers=headers)
    a =(response.json())
    return (a['result'])
# b = order_finished_extra_access(931184)
# print(b)


def Binance_Market_order_Buy(market_name,qty):
    client = Client(Binance_Api_key,Binance_Api_Secret)
    order = client.order_market_buy(symbol=market_name,quantity=qty)
    print(order)
    
def Binance_Market_order_Sell(market_name,qty):
    client = Client(Binance_Api_key,Binance_Api_Secret)
    order = client.order_market_sell(symbol=market_name,quantity=qty)
    print(order)


# In[ ]:


from websocket import create_connection
ws = create_connection("wss://tsocket.cryptokart.io:453")
print(ws)
ws.send(json.dumps({"id":1,"method":'server.sign',"params":[client_id,client_secret,timestamp]}))
dict = {}

while(True):
    try:
            
        
        b =ws.send(json.dumps({"id":1,"method":'order.subscribe',"params":["BTCUSDT"]}))
        result = (ws.recv())
        a = (json.loads(result))
    #     print(b)
    #     time.sleep(1)
        if("method" in a):
    #         print(result)
            if((a["params"][0])==2):                                                  #Check param id ==2
                id = a["params"][1]["id"]
                deal_id = order_deals_postman(client_id,client_secret,id,0,10)
                deal_order_id = deal_id[0]['deal_order_id']
                price =deal_id[0]['price']
                amount = deal_id[0]['amount']
                Final_data= order_finished_extra_access(deal_order_id)
                if(Final_data['user'] == 49):
                    print("This crazy bot filling order partially")
                else:
                    print("Placing order on Binance with partial filled price and amount",price,amount)
                    if((Final_data['side'])==1):
                        Binance_Market_order_Sell(market_name,amount)
                    elif(Final_data('side')== 2):
                        Binance_Market_order_Buy(market_name,amount)
                    else:
                        print("This can't happen, OUT OF BOX... Something went crazy")
            elif((a["params"][0])==3):
                id = a["params"][1]["id"]
                order_deals = order_deals_postman(client_id,client_secret,id,0,10)
                if(len(order_deals) == 0):
                    print("Order get cancelled without getting even a single fill")
                else:
                    deal_order_id = order_deals[0]['deal_order_id']
                    price =order_deals[0]['price']
                    amount = order_deals[0]['amount']
                    res = order_finished_detail_postman(client_id,client_secret,id)
                    ftime = res['ftime']
                    time = order_deals[0]['time']
                    if(ftime == time):
                        check_user = order_finished_extra_access(deal_order_id)
                        if(check_user['user'] == 49):
                            print("Order get filled by our bot at price and amount",price,amount)
                        else:
                            print("Order get filled by some Real user at price and amount",price ,amount)
                            if((check_user['side'])==1):
                                Binance_Market_order_Sell(market_name,amount)
                            elif(check_user('side')== 2):
                                Binance_Market_order_Buy(market_name,amount)
                            else:
                                print("This can't happen, OUT OF BOX... Something went crazy")
                    else:
                        print("Order get cancelled after some filling has been done")
                        
            else:
                print("Breath IN Breath OUT.. order place hua hai bss")
                            
    except Exception as e:
            print("EXception aaya Bhaggoooo !!!!!!! \n \n \n")
            print(e)
            continue    


  

ws.close()



