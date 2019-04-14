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


# This function is provided with python-binance in order to get data you have to pass Keys here
#For more info go to this URl -> https://python-binance.readthedocs.io/en/latest/binance.html
client = Client("Binance API key","Binance Secret Key")    #No need to provide key here in this file as we are using only public data's

def Market_Price_Binance():
    prices = client.get_all_tickers()
    if(prices[190]['symbol']== 'LTCUSDT'):                    #Change this to get different LTP for diff market
        LTP_Binance = float(prices[190]['price'])
        print("Market price of LTCUSDT -> ", LTP_Binance)
        return LTP_Binance
LTP = Market_Price_Binance()                                       #This value is used in variable Price regulator





# In[3]:


#Variable Declaration
client_id ="8"                              # Provide API client ID to access the data
client_secret= "0e92618345c7b"                         # Provide API client secret key to access the data
market_name = "LTCUSDT"                                    # Enter the Market Name you want to trade in
CK_url = "https://test.cryptokart.io:1337/"                # Change this URL to go from Staging to Production


# In[4]:


# Pre defined variable , edit with your atmost attention.
# Link of spreadsheet with all details https://docs.google.com/spreadsheets/d/11mmmC_z8oau-EAznqgOeOiVX-5ZOPs7UTav-WwBLjqY/edit#gid=1364363676

# Every order amount should be around this average price in USDT
avg_trade_price = 40    

# 24 hour volume you want IN USDT
expected_24_hr_volume = 5000

# After this time , script will reset default 24 hrs = 86400
give_time_to_generate_volume = 86400


# This will make difference b/w half past like 12:28 - 12:30
time_delay_for_half_past = 130

# this is int value for how many hours you want half past timestamp
hours_timestamp = 24


min_value = 7                                     # The order amount should not be less than this. (IN USDT)
randomness_factor = 500                           # This will make for looop run this times, to create randomness for amount generation


round_off_factor_amount = 3                       # This is to round off amount


# In[ ]:



# Functions

# Func(1) -> It will place a market order to the specified amount
def FireOrder_Market(client_id,client_secret,market_name,side,amount):
    url =CK_url+"matchengine/order/putMarket"
    payload=({"client_id":client_id,"client_secret": client_secret,"market_name": market_name,"side": side,"amount": amount})
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    print(response.json())

# FireOrder_Market(client_id,client_secret,market_name,1,"0.001")


# In[ ]:


# This function have all the logic, it will generate static time amount and place the orders.
def Trade_Order_Market():
    try:
        
        while(True):

            # time_list is empty array, this will have all the timestamps at later stage
            # This array contains all the timestamps at which order will be placed
            n = 0
            time_list = []                                              
            List_order_amounts = []
            temp = 0




            LTP = Market_Price_Binance()
            print("\n \n Last Traded Price is \t ", LTP)

            # Now we will gwnerate the number of trades that we required
            # We are subtracting 48 because 48 orders are reserved to place at :30
            num_of_trades_per_day = int(expected_24_hr_volume / avg_trade_price)  - (hours_timestamp *2)       # eg -> 5000/60 = 83.33


            # ---------- To make sure it is even . so that balance can be maintained .. we are doing this -----------
            if((num_of_trades_per_day % 2) == 0):
                pass
            else:
                num_of_trades_per_day -= 1

            #-----------------------------------------------------------------------------------------------------------


            # --------------------Finding current timestamp and finding exact minutes that is right now-----------------
            # -----------------------------This will help us to place order around :30-------------------------------------
            current_timestamp = time.time()
            current_timestamp = (int(round(current_timestamp)))
    #         print(current_timestamp)
            minutes = int(datetime.datetime.fromtimestamp(current_timestamp).strftime('%M'))
            print("\n \n See the clock current minutes are \t",minutes)

            #-----------------------------------------------------------------------------------------------------------


            if (minutes > 29):
                temp = (60 - minutes)+29
                print("\n This much time is left to make it half past O'clock \t",temp)
            elif(minutes < 29):
                temp = (29 - minutes)
                print("\n This much time is left to make it half past O'clock \t",temp)
            else:
                temp = 0

            # I have added extra minutes to current ts , so that it can make it to exact half past O'clock
            timestamp = current_timestamp + (temp * 60)
            estimated_time = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
            print("\n Thsi will be the time through which cycle of half past starts \t",estimated_time)


            # Will generate timestamp for before half past O'clock ,            eg before 11:30

            while(n < hours_timestamp):
                random_time = int(random.randint(timestamp - time_delay_for_half_past,timestamp))
                if (random_time not in time_list):
                    time_list.append(random_time)
                    n = n+1
                timestamp = timestamp +3600                                    # This increased the clock to 1 hour straight
            b =[]
            for i in range(hours_timestamp):
                a = time_list[i]
                st = datetime.datetime.fromtimestamp(a).strftime('%Y-%m-%d %H:%M:%S')
                b.append(st)
            b.sort()
            print("\n \n This is first timestamp array \t \n",b)



            # Will generate timestamp for after half past O'clock

            # Reinitialized the timestamp to reset the value to current timestamp
            timestamp = current_timestamp + (temp * 60)
            n= 0

            while(n <hours_timestamp):
                random_time = int(random.randint(timestamp +40,timestamp + 129))
                if (random_time not in time_list):
                    time_list.append(random_time)
                    n = n+1
                timestamp = timestamp +3600
            print(len(time_list),"\t  \t AB 48 orders hogye place")
            b =[]
            for i in range((hours_timestamp*2)):
                a = time_list[i]
                st = datetime.datetime.fromtimestamp(a).strftime('%Y-%m-%d %H:%M:%S')
                b.append(st)
            b.sort()
            print("\n \n  This was timestamp before and after half past O'clock \t",b)



            #--------------------------------------------------------------------------------------------------------
            print("---------------------|||||||||||||||||||||||||||||||||||---------------------------------------||||||||||||||||||||||||||||||||||-----------------------")


            # Now we will generate timestamps for remaining hour and trade that will be totally random

            # Just printing and generating current Timestamp and timestamp after certain period of time.
            current_timestamp = time.time()
            current_timestamp = (int(round(current_timestamp)))
            st = datetime.datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print ("\n \n CURRENT TIME AND DATE \t \t \t \t",st)

            timestamp_aft_24hrs = time.time() + give_time_to_generate_volume
            timestamp_aft_24hrs = (int(round(timestamp_aft_24hrs)))
            st = datetime.datetime.fromtimestamp(timestamp_aft_24hrs).strftime('%Y-%m-%d %H:%M:%S')
            print ("\n \n TIME AND DATE  AFTER 24(DEFAULT) HOURS \t",st)



            length_time_list = 0

            # This is how I generated different timestamp in a day.
            while(num_of_trades_per_day > length_time_list):
                random_time = int(random.randint(current_timestamp,timestamp_aft_24hrs))
                if (random_time not in time_list):
                    time_list.append(random_time)
                    length_time_list = len(time_list)

            time_list.sort()
        #     print(time_list,"\n \n \n")

            # If you want to watch the timestamp in IST, with dates just uncomment the next 7 lines and run it again
            b =[]
            for i in range(len(time_list)):
                a = time_list[i]
                st = datetime.datetime.fromtimestamp(a).strftime('%Y-%m-%d %H:%M:%S')
                b.append(st)
            print("\n \n -------------------------------------------------------------------------------- \n \n")
            print("\n \nAt this time all order will be placed \n \t",b)
            print("\n \n ----------------------------------------------------------------------------------------------- \n \n")


             # List to generate buy and sell side

            volume_each_side = (expected_24_hr_volume / 2)    # Buy and sell side will generate this much volume
            order_each_side = int(num_of_trades_per_day /2)   # Each side number of orders will be

            print("\n \n \t Each will have volume \t ", volume_each_side ,"/t and order", order_each_side)


            avg_order_amount = volume_each_side / order_each_side
            print(" AVERAGE ORDER AMOUNT /t ",avg_order_amount)

            LB_range = (avg_order_amount * 5)/100
            UB_range = (avg_order_amount * 70)/100

            # just to create a list of buy and sell with equal average amount, now we have to modify it
            buy_amount_arr = [avg_order_amount] * order_each_side
            sell_amount_arr = [avg_order_amount] * order_each_side




            # This have created random amount in array with fix mean
            # Taking a random amount .. adding some amount to it and subtracting exactly same amount from other
            # So that mean remain same.. and in the end taking care amount should not be negative so, checking that
            for i in range(randomness_factor):
                take_random_number = random.choice(buy_amount_arr)
                temp_storage = take_random_number
                buy_amount_arr.remove(take_random_number)
                random_delta = random.uniform(LB_range,UB_range)
                temp_storage += random_delta
                buy_amount_arr.append(temp_storage)
                take_random_number = random.choice(buy_amount_arr)
                if((take_random_number- random_delta) > min_value):
                    buy_amount_arr.remove(take_random_number)
                    take_random_number = take_random_number - random_delta
                    buy_amount_arr.append(take_random_number)
                else:
                    buy_amount_arr.remove(temp_storage)
                    temp_storage -= random_delta
                    buy_amount_arr.append(temp_storage)
    #         print("\n \n This is magical array \n \n")
            random.shuffle(buy_amount_arr)
        #     print(buy_amount_arr)

            length_buy_array = len(buy_amount_arr)


            # To check whether mean is right or not just uncomment it.
        #     a =0
        #     for i in range(len(buy_amount_arr)):
        #         a = a + buy_amount_arr[i]
        #     b = a / len(buy_amount_arr)
        #     print(b)


        # Now we will modify array in terms of local cryptocurrency amount
            ltp = Market_Price_Binance()
            for i in range(len(buy_amount_arr)):
                buy_amount_arr[i] = round((buy_amount_arr[i] / ltp),round_off_factor_amount)
            print("Buy array modified version \t ",buy_amount_arr)


            # Same procedure for Sell array
            for i in range(randomness_factor):
                take_random_number = random.choice(sell_amount_arr)
                temp_storage = take_random_number
                sell_amount_arr.remove(take_random_number)
                random_delta = random.uniform(LB_range,UB_range)
                temp_storage += random_delta
                sell_amount_arr.append(temp_storage)
                take_random_number = random.choice(sell_amount_arr)
                if((take_random_number- random_delta) > min_value):
                    sell_amount_arr.remove(take_random_number)
                    take_random_number = take_random_number - random_delta
                    sell_amount_arr.append(take_random_number)
                else:
                    sell_amount_arr.remove(temp_storage)
                    temp_storage -= random_delta
                    sell_amount_arr.append(temp_storage)
    #         print("\n \n This is magical array \n \n")
            random.shuffle(sell_amount_arr)
        #     print(sell_amount_arr)
            length_sell_array = len(sell_amount_arr)

        #     a =0
        #     for i in range(len(sell_amount_arr)):
        #         a = a + buy_amount_arr[i]
        #         b = a / len(sell_amount_arr)
        #     print(b)

            ltp = Market_Price_Binance()
            for i in range(len(sell_amount_arr)):
                sell_amount_arr[i] = round((sell_amount_arr[i] / ltp),round_off_factor_amount)
            print(" \n Modified version for sell array \t ",sell_amount_arr)


            # ---------------------------------------------------------------------------------------------------------
            # Till now we have created static timestamp and buy sell array, now just we have to place order randomly as per timestamsp



            current_timestamp = (int(round(time.time())))
            print(current_timestamp)
            print(len(time_list),"Time list")
            n = 0



            for i in range(len(time_list)):
                print("script started", i , time)
                ts_order_place = time_list[i]
                diff = (ts_order_place - current_timestamp)
                print("\n Order will place after \t  ", diff, "seconds")
                time.sleep(diff)


                a = random.randint(1,2)
                if(a == 1):
                    if (n < length_sell_array):
                        val_amt = (sell_amount_arr[0])
                        amt = str(sell_amount_arr[0])
                        FireOrder_Market(client_id,client_secret,market_name,1,amt)
                        sell_amount_arr.remove(val_amt)
                        n = n+1
                    else:
                        val_amt = (buy_amount_arr[0])
                        amt = str(buy_amount_arr[0])
                        FireOrder_Market(client_id,client_secret,market_name,2,amt)
                        buy_amount_arr.remove(val_amt)
                elif(a == 2):
                    if (n < length_buy_array):
                        val_amt = (buy_amount_arr[0])
                        amt = str(buy_amount_arr[0])
                        FireOrder_Market(client_id,client_secret,market_name,2,amt)
                        buy_amount_arr.remove(val_amt)
                        n = n+1
                    else:
                        val_amt = (sell_amount_arr[0])
                        amt = str(sell_amount_arr[0])
                        FireOrder_Market(client_id,client_secret,market_name,1,amt)
                        sell_amount_arr.remove(val_amt)

                current_timestamp = time_list[i]

            
    except Exception as e:
        print(e)
        pass





Trade_Order_Market()



        
        


# In[ ]:




