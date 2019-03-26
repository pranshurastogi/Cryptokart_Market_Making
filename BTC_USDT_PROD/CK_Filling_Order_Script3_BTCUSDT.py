#!/usr/bin/env python
# coding: utf-8

# In[1]:


# By - Pranshu Rastogi
# Market making strategy

# Importing libraries
import requests
import random
import json
import time
import datetime
import sys
from binance.client import Client
from binance.enums import *


# In[2]:


#Variable Declaration
client_id = "Insert API KEY"                                 # Provide API client ID to access the data
client_secret= "Insert Secret KEY"                          # Provide API client secret key to access the data
market_name = "BTCUSDT"                                    # Enter the Market Name you want to trade in 
CK_url = "https://test.cryptokart.io:1337/"                # Change this URL to go from Staging to Production


# In[ ]:


# Variable Declaration -> Please fill variables carefully by reading comments and after having a cup of coffee.

# The upcoming two variables -> (long_time_delay_LB , long_time_delay_UB) will provide delay between this range
# This is basically to provide large time gap randomly
# Please provide input in seconds -> Default LB = 2400 (40 minutes), UB = 3600(60 minutes)
long_time_delay_LB = 2400                                     # Seconds for long time sleep Lower bound
long_time_delay_UB = 3600                                     # Seconds for long time sleep Upper bound


give_time_to_generate_volume = 86400                          #Volume timer for 24 hours (24 hours = 86400 seconds)
volume_we_need_24_hrs = 20                                    # It is the volume in BTC or crypto asset that we need in 24 hr volume

# This will provide probability or approximate percentage to place regular order to long sleep function
prob_long_time_and_reg_order = 0.7                           #Range b/w [0.0 to 1.0] Default 0.7


# In[ ]:


# Functions 

# Func(1) -> It will place a market order to the specified amount
def FireOrder_Market(client_id,client_secret,market_name,side,amount):
    url ="https://test.cryptokart.io:1337/matchengine/order/putMarket"
    payload=({"client_id":client_id,"client_secret": client_secret,"market_name": market_name,"side": side,"amount": amount})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.text)
    
    
# fUNC(2) -> it will provide sleep time for a long period without placing any order
def Long_Time_Delay(long_time_delay_LB,long_time_delay_UB):
    sleep_time = random.randint(long_time_delay_LB,long_time_delay_UB)
    print("\n \n This is rare case and now NO order will place for ",sleep_time/60," Minutes")
    time.sleep(sleep_time)
    
    
    
# Func(3) -> It will provide current timestamp and timestamp after 24 hours, you can adjust 24 hours variable            
def Timestamp_Calculator():
    current_timestamp = time.time()
    current_timestamp = (int(round(current_timestamp)))
    st = datetime.datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print (st,"\n \n \t CURRENT TIME AND DATE \N \N")
    timestamp_aft_24hrs = time.time() + give_time_to_generate_volume
    timestamp_aft_24hrs = (int(round(timestamp_aft_24hrs)))
    st = datetime.datetime.fromtimestamp(timestamp_aft_24hrs).strftime('%Y-%m-%d %H:%M:%S')
    print (st,"\n \n \t  TIME AND DATE  AFTER 24(DEFAULT) HOURS\N \N")
    return current_timestamp,timestamp_aft_24hrs
    


# In[32]:


def Trade_Order_market():
    
    timestamp = Timestamp_Calculator()                             # Taking curr timestamp and 24 hrs timestamp for first tiem 
    curr_ts = timestamp[0]
    ts_after_Day = timestamp[1]
    
    counter_long_time_delay = 0                                    # Initialising 0 for start , to keep track of Long_Time_Delay() execution 
    volume_24_hrc_checker = 0                                      # Initialising 0 for start, to keep track of 24 hr volume
    
    while(True):
        try:
            # Next line will check whether this will loop is running less than 24 hrs or more
            if(curr_ts < ts_after_Day):
                
                #Next line will track the total volume that we will consume
                if (volume_24_hrc_checker < volume_we_need_24_hrs):
                    
                    # This is to provide probability to run regular orders and long time sleep func
                    probability_variance = random.random()
                    if (probability_variance < prob_long_time_and_reg_order):
                        
                        probability_generator = random.random()
                        if (probability_generator < 0.8):
                            random_sleep_time = random.randint(15,30)
                            for i in range(1,3):
                                random_amount = random.uniform(1,6)
                                volume_24_hrc_checker = volume_24_hrc_checker + random_amount
                                buy_sell_decider =random.randint(1,2)                # Aapka adviser.. Will tell you -> Buy or Sell
                                FireOrder_Market(client_id,client_secret,"BTCUSDT",buy_sell_decider,random_amount)
                            time.sleep(random_sleep_time)


                        else:
                            random_sleep_time = random.randint(15,30)
                            order_hit_no = random.randint(1,4)                       # Number of Large amount orders it will hit...
                            for i in range(order_hit_no):
                                random_amount = random.uniform(1,6)
                                mul_factor = random.randint(3,6)                     # It's like a hulk .. increasing order amount size  (depend kitna gussa aaya hulk ko {Random})
                                big_amt = random_amount * mul_factor                 # Complan taken -> Amount size increased
                                volume_24_hrc_checker = volume_24_hrc_checker + big_amt
                                buy_sell_decider =random.randint(1,2)                # Aapka adviser.. Will tell you -> Buy or Sell
                                FireOrder_Market(client_id,client_secret,"BTCUSDT",buy_sell_decider,big_amt)  # Finally Market Order Placed
                            time.sleep(random_sleep_time)
                    else:
                        if(counter_long_time_delay < 4):
                            Long_Time_Delay()
                            counter_long_time_delay += 1
                else:
                    sleeper_cell = (ts_after_Day - curr_ts)
                    time.sleep(sleeper_cell)

            else:
                timestamp = Timestamp_Calculator()
                curr_ts = timestamp[0]
                ts_after_Day = timestamp[1]
                counter_long_time_delay = 0

                volume_24_hrc_checker = 0
        except KeyboardInterrupt:
            print ("May the force with you")
            sys.exit()
        except Exception as e:
            print("\n \n \t \t EXCEPTION FOUND !! BE CAUTIOUS \n \n \n")
            print(e)
            continue


    
Trade_Order_market()
    


# In[3]:


a =3
print("fffff",a*3,"ddd")


# In[ ]:




