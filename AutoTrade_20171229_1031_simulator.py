
# coding: utf-8

# In[ ]:


import sys


# In[ ]:


def get_markets_list(base_coin = 'USDT'):
    from bittrex.bittrex import Bittrex, API_V1_1, API_V2_0

    API_V20 = Bittrex('','',api_version=API_V2_0)
    API_V11 = Bittrex('','',api_version=API_V1_1)
    
    markets_list = []

    market_sum = API_V20.get_market_summaries()
    markets_all_list = market_sum['result']
    for market_ in markets_all_list:
        if market_['Market']['BaseCurrency'] == base_coin:
            markets_list.append(market_['Market']['MarketName'])
    return markets_list


# In[ ]:


def find_buy_point_in_all_markets(markets_list, time_interval, N_candle = 200, method = 'macd_cross'):
    for market_ in markets_list:
        bs_point = find_buy_sell_point(market_, time_interval)
        if bs_point['b_macd_buy'] == 1:
            print('a buy point is just identified among the markets list.')
            print(bs_point)
            return bs_point


# In[6]:


-


# In[ ]:


def check_buy_point(buy_point):
    #do nothing for now
    #future check current price to ema
    #also 
    print('a buy point is triggered.')
    return buy_point['b_macd_buy']


# In[ ]:


def set_buy_point(market_, price, money, price_offset_factor = 0.99):
    from bittrex.bittrex import Bittrex, API_V1_1, API_V2_0
    API_V20 = Bittrex('','',api_version=API_V2_0)
    API_V11 = Bittrex('','',api_version=API_V1_1)
    
    # place a buy order， price could be lower than macd price
    buy_price = price*price_offset_factor
    buy_amount = money/buy_price
    while(1):
        text = '>>>>>>>>>>>' + market_ + ": place a buy order of amount of" + str(buy_amount) + "@$" + str(buy_price)
        print(text)
        # place order(market_, price, amount)
        # check respond
        # take care of double order
        if (1):
            break
            
    # leave a record
    buy_set_info = dict()
    buy_set_info['market_'] = market_
    buy_set_info['price'] = buy_price
    buy_set_info['amount'] = buy_amount
    buy_set_info['activity'] = 'buy_set'
    buy_set_info['time'] = API_V11.get_marketsummary(market='USDT-OMG')['result'][0]['TimeStamp']
    return buy_set_info


# In[ ]:


def check_buy_filled(market_, set_buy_price, set_buy_amount):
    # for simulation, get current price, if it is below the previous price, then filled
    # for real situation sen request.
    from bittrex.bittrex import Bittrex, API_V1_1, API_V2_0
    API_V20 = Bittrex('','',api_version=API_V2_0)
    API_V11 = Bittrex('','',api_version=API_V1_1)

    current_price = API_V11.get_marketsummary(market='USDT-OMG')['result'][0]['Last']
    if (current_price<set_buy_price):
        buy_set_info = dict()
        buy_filled_info['market_'] = market_
        buy_filled_info['price'] = set_buy_price
        buy_filled_info['amount'] = set_buy_amount
        buy_filled_info['activity'] = 'buy_filled'
        buy_filled_info['time'] = API_V11.get_marketsummary(market='USDT-OMG')['result'][0]['TimeStamp']
        return buy_filled_info
    else:
        buy_set_info = dict()
        buy_filled_info['activity'] = 'buy_not_filled'
        return buy_filled_info
        
    


# In[ ]:


def check_if_reset_buy(market_, time_interval):
    sell_point = find_buy_sell_point(market_, time_interval)
    #do nothing for now
    #future check current price to ema
    #also 
    b_reset_buy = sell_point['b_macd_sell']
    return b_reset_buy


# In[ ]:


def reset_buy():
    #while until reset


# In[ ]:


def check_sell_point(sell_point):


# In[ ]:


def set_sell_point(market_, price, price_offset_factor = 0.99)


# In[ ]:


def check_sell_filled():


# In[ ]:


def check_if_reset_sell(sell_point, reset_sell_point):


# In[ ]:


def reset_sell():
    #while until reset


# In[ ]:


b_buy_enabled = False
b_buy_tigger = False
b_buy_tigger = False
b_buy_set = False
b_reset_buy = False

b_sell_enabled = False
b_sell_tigger = False
b_sell_tigger = False
b_sell_set = False
b_reset_sell = False

record_list = []
previous_buy_price = sys.float_info.max
market_ = ""
previous_buy_price = 0
set_sell_price = 0
time_interval = 'oneMin'

markets_list = get_markets_list(market_platform, base_coin = 'USDT')

if b_buy_enabled:
    if not(b_buy_set):
        # find buy point @ all markets
        buy_point = find_buy_point_in_all_markets(markets_list, time_interval, method = 'macd_cross')
        b_buy_trigger = check_buy_point(buy_point)
        
    if b_buy_trigger:
        market_ = buy_point['market_']
        price = buy_point['current_price']
        buy_set_info = set_buy_point(market_, price, price_offset_factor = 0.99)
        
        buy_set_info['bs_point'] = buy_point
        record_list.append(buy_set_info)
        b_buy_trigger = False
        b_buy_set = True
    
    if b_buy_set:
        reset_buy_point = find_buy_sell_point(market_, time_interval)
        buy_filled_info = check_buy_filled()
        record_list.append(buy_filled_info)
            #information from market platform
        if b_buy_filled:
            #leave a record
            b_sell_enabled = True
            b_buy_enabled = False
            b_buy_set = False
            continue
        b_reset_buy = check_if_reset_buy(buy_point, reset_buy_point)
        if b_reset_buy:
            buy_filled_info = reset_buy()
                # cancel buy order
                # leave a record

if b_sell_enabled:
    if not(b_sell_set)
        # find sell point @ all markets
        info_from_other_market = check_info_from_other_market(platform_market_list)
            #do nothing for now
        sell_point = find_sell_point(markets_, method = 'macd_cross')
            #macd
        b_sell_trigger = check_sell_point(sell_point, info_from_other_market)
            #do nothing for now
            #future check current price to ema
            #also 
        
    if b_sell_trigger:
        price = sell_point['price']
        record = set_sell_point(market_, price, price_offset_factor = 0.99)
            # place a sell order， price could be higher than macd price
            # leave a record
        b_sell_trigger = False
        b_sell_set = True
    
    if b_sell_set:
        reset_sell_point = find_buy_point(market_, method = 'macd_cross')
            #macd
        b_sell_filled = check_sell_filled
            #information from market platform
        if b_sell_filled:
            #leave a record
            b_buy_enabled = True
            b_sell_enabled = False
            b_sell_set = False
            continue
        
        b_reset_sell = check_if_reset_sell(sell_point, reset_sell_point)
            #do nothing for now
            #future check current price to ema
            #also 
        if b_reset_sell:
            record = reset_sell()
                # cancel sell order
                # leave a record
        
        
        
        
        
        
        
    


# In[ ]:


from get_info_from_bittrex_py import getCandleFromBittrex
from stock_index_functions import process_candle_result, display_candle_volume_macd

candle_result = getCandleFromBittrex("USDT-OMG", time_interval="oneMin")
processed_candle_result = process_candle_result(candle_result)
fig1=display_candle_volume_macd(candle_result)

