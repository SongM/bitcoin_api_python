
# coding: utf-8

# In[1]:


from get_info_from_bittrex_py import getCandleFromBittrex
from stock_index_functions import process_candle_result, display_candle_volume_macd

candle_result = getCandleFromBittrex("USDT-OMG", time_interval="Hour")
processed_candle_result = process_candle_result(candle_result)
##fig1=display_candle_volume_macd(candle_result)


# In[2]:


def get_buy_sell_point(diff_privious, diff_current, current_price,
                       previous_activity_type, previous_activity_price,
                       method, fee_rate=0.999, stop_loss_rate = 0.9):
    
    result = dict()

    if (method == "macd_cross"):
        sell_trigger = (diff_privious>0) and (diff_current<0)
        buy_trigger = (diff_privious<0) and (diff_current>0)
    if (method == "rand"):
        import random
        sell_trigger = random.random()>0.5
        buy_trigger = random.random()>0.5
        
    # make sure no money is loss
#    buy_trigger = buy_trigger and current_price<previous_activity_price*fee_rate
    sell_trigger = sell_trigger and current_price>previous_activity_price/fee_rate
    
    # stop loss
    sell_trigger = sell_trigger or current_price<previous_activity_price*stop_loss_rate
        
    # check privious activity
    buy_trigger = buy_trigger and previous_activity_type!='buy'
    sell_trigger = sell_trigger and previous_activity_type!='sell'

    result['sell_trigger'] = sell_trigger
    result['buy_trigger'] = buy_trigger
    result['stop_loss'] = sell_trigger and current_price<previous_activity_price*stop_loss_rate
    return result


    money = 1
    coin = 0
    activity_list = []

    previous_activity_price = 99999999999
    previous_activity_type = 'sell'
    for i in range (62,len(processed_candle_result['bar_diff_14_30_dea_10'])):
        diff_privious = processed_candle_result['bar_diff_14_30_dea_10'][i-1]
        diff_current = processed_candle_result['bar_diff_14_30_dea_10'][i]
        current_price = candle_result['closep'][i]
        current_date = candle_result['date'][i]

        trigger_result = get_buy_sell_point(diff_privious, diff_current, current_price,
                           previous_activity_type, previous_activity_price,
                           method, fee_rate=0.99, stop_loss_rate = 0.9)

        sell_trigger = trigger_result['sell_trigger']
        buy_trigger = trigger_result['buy_trigger']

        if not(sell_trigger or buy_trigger):
            continue

        activity = dict()
        activity['price'] = current_price
        activity['date'] = current_date
        activity['stop_loss'] = trigger_result['stop_loss']


        if sell_trigger == 1:
            money = coin*current_price*0.9975
            coin = 0
            activity['type'] = "sell"
            previous_activity_type = 'sell'

        if buy_trigger == 1:
            coin = money/current_price*0.9975
            money = 0
            activity['type'] = "buy"
            previous_activity_type = 'buy'


        activity['money'] = money
        activity['coin'] = coin
        activity['value'] = coin*current_price + money
        previous_activity_price = current_price
        if trigger_result['stop_loss']:
            previous_activity_price = 99999999999
        activity_list.append(activity)


        buy_trigger = 0
        sell_trigger = 0
    return activity_list

        


# In[3]:


def autotrade_simulator(candle_result, processed_candle_result, method):

    money = 1
    coin = 0
    activity_list = []

    previous_activity_price = 99999999999
    previous_activity_type = 'sell'
    for i in range (62,len(processed_candle_result['bar_diff_14_30_dea_10'])):
        diff_privious = processed_candle_result['bar_diff_14_30_dea_10'][i-1]
        diff_current = processed_candle_result['bar_diff_14_30_dea_10'][i]
        current_price = candle_result['closep'][i]
        current_date = candle_result['date'][i]

        trigger_result = get_buy_sell_point(diff_privious, diff_current, current_price,
                           previous_activity_type, previous_activity_price,
                           method, fee_rate=0.99, stop_loss_rate = 0.9)

        sell_trigger = trigger_result['sell_trigger']
        buy_trigger = trigger_result['buy_trigger']

        if not(sell_trigger or buy_trigger):
            continue

        activity = dict()
        activity['price'] = current_price
        activity['date'] = current_date
        activity['stop_loss'] = trigger_result['stop_loss']


        if sell_trigger == 1:
            money = coin*current_price*0.9975
            coin = 0
            activity['type'] = "sell"
            previous_activity_type = 'sell'

        if buy_trigger == 1:
            coin = money/current_price*0.9975
            money = 0
            activity['type'] = "buy"
            previous_activity_type = 'buy'


        activity['money'] = money
        activity['coin'] = coin
        activity['value'] = coin*current_price + money
        previous_activity_price = current_price
        if trigger_result['stop_loss']:
            previous_activity_price = 99999999999
        activity_list.append(activity)


        buy_trigger = 0
        sell_trigger = 0
    return activity_list

        


# In[4]:


# scan all
from get_info_from_bittrex_py import getCandleFromBittrex
from bittrex.bittrex import Bittrex, API_V1_1, API_V2_0
import csv

API_V20 = Bittrex('','',api_version=API_V2_0)
API_V11 = Bittrex('','',api_version=API_V1_1)

market_sum = API_V20.get_market_summaries()
market_list = market_sum['result']
with open('temp_market_summary_2.csv', 'w') as csvfile:
    output_csv = dict();

    output_csv['market'] = 1
    output_csv['coin_exchange'] = 1
    output_csv['coin_base'] = 1
    output_csv['macd_profit'] = 1
    output_csv['last_trade_price_to_current_ema_7'] = 1
    output_csv['last_trade_price_to_current_ema_14'] =1
    output_csv['last_trade_price_to_current_ema_30'] = 1
    output_csv['last_trade_price_to_current_ema_60'] = 1
    output_csv['BaseVolume'] = 1
    output_csv['recentPrice'] = 1
    output_csv['OpenBuyOrders'] = 1
    output_csv['OpenSellOrders'] = 1
    output_csv['ratio_BS'] = 1
    output_csv['N_macd_trade'] = 1

    fieldnames = output_csv.keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for t in market_list:
        market_=t['Market']['MarketName']
        from get_info_from_bittrex_py import getCandleFromBittrex
        from stock_index_functions import process_candle_result, display_candle_volume_macd
        candle_result = getCandleFromBittrex(market_, time_interval="oneMin" ,N_max_candle=400)
        processed_candle_result = process_candle_result(candle_result)



        closep = candle_result['closep']
        one_trade_max_profit = max(closep)/min(closep)-1

        macd_activity_list = autotrade_simulator(candle_result, processed_candle_result, method="macd_cross")
        macd_profit = macd_activity_list[-1]['money'] + closep[-1]*macd_activity_list[-1]['coin'] -1

        rand_profit=[]
        for i in range(1,10):
            activity_list = autotrade_simulator(candle_result, processed_candle_result, method="rand")
            rand_profit.append(activity_list[-1]['money'] + closep[-1]*activity_list[-1]['coin'] -1)
        text = 'macd_profit = ' + str(macd_profit)
        text += ', N_macd_trade = ' + str(len(macd_activity_list))
        text += '\n, macd_profit v.s one_trade_max_profit = ' + str(macd_profit/one_trade_max_profit)
        text += ', max_rand_profit_in_100_trial = ' + str(max(rand_profit)/one_trade_max_profit)
        print(text)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        output_csv = dict();
        output_csv['market'] = market_
        output_csv['coin_exchange'] = candle_result['coin_exchange']
        output_csv['coin_base'] = candle_result['coin_base']
        output_csv['macd_profit'] = macd_profit
        output_csv['N_macd_trade'] = len(macd_activity_list)
        output_csv['last_trade_price_to_current_ema_7'] = processed_candle_result['last_trade_price_to_current_ema_7']
        output_csv['last_trade_price_to_current_ema_14'] = processed_candle_result['last_trade_price_to_current_ema_14']
        output_csv['last_trade_price_to_current_ema_30'] = processed_candle_result['last_trade_price_to_current_ema_30']
        output_csv['last_trade_price_to_current_ema_60'] = processed_candle_result['last_trade_price_to_current_ema_60']
        output_csv['BaseVolume'] = candle_result['market_summary']['result'][0]['BaseVolume']
        output_csv['recentPrice'] = candle_result['market_summary']['result'][0]['Last']
        output_csv['OpenBuyOrders'] = candle_result['market_summary']['result'][0]['OpenBuyOrders']
        output_csv['OpenSellOrders'] = candle_result['market_summary']['result'][0]['OpenSellOrders']
        output_csv['ratio_BS'] = float(output_csv['OpenBuyOrders'])/output_csv['OpenSellOrders']



        writer.writerow(output_csv)

print('done')


# In[5]:


candle_result['market_summary']


# In[6]:


import numpy as np
print np.mean(rand_profit)


# In[7]:


np.sum(np.positive(rand_profit)>0)


# In[8]:


a='2017-12-29T03:29:07'


# In[9]:


datetime.strptime(a, '%Y-%m-%dT%H:%M:%S.%f')


# In[ ]:


import csv
output_csv = dict();
output_csv['market'] = market_
output_csv['coin_exchange'] = candle_result['coin_exchange']
output_csv['coin_base'] = candle_result['coin_base']
output_csv['macd_profit'] = macd_profit
output_csv['last_trade_price_to_current_ema_7'] = processed_candle_result['last_trade_price_to_current_ema_7']
with open('temp_market_summary.csv', 'w') as csvfile:
    fieldnames = output_csv.keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow(output_csv)
    


# In[ ]:


market_

