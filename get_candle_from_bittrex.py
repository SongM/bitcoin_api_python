
# coding: utf-8

# In[8]:


# bittrex

coin_base = "USDT"
coin_exchange = "OMG"
coin_base = "ETH"
coin_exchange = "ENG"
market_ = coin_base + "-" + coin_exchange
print market_
time_interval = "thirtyMin"
N_start_ind = 1908;
N_max_candle = 200;
N_min_candle = 10;

#def getCandleFromBittrex(coin_base, coin_exchange, market_,
 #                        time_interval, N_start_ind, N_max_candle, N_min_calde):

import matplotlib.dates as dt
from datetime import datetime
from bittrex.bittrex import Bittrex, API_V1_1, API_V2_0
from bittrex.bittrex import BUY_ORDERBOOK, SELL_ORDERBOOK, BOTH_ORDERBOOK



result = dict()
result['marketPlatform'] = 'bittrex'
result['market_'] = market_
result['coin_base'] = coin_base
result['coin_exchange'] = coin_exchange
result['time_interval'] = time_interval
result['N_start_ind'] = N_start_ind
result['N_max_candle'] = N_max_candle
result['N_min_candle'] = N_min_candle



API_V20 = Bittrex('','',api_version=API_V2_0)
API_V11 = Bittrex('','',api_version=API_V1_1)


# get candle, generate ohlc
candles = API_V20.get_candles(market_, tick_interval=time_interval)
latest_candle = API_V20.get_latest_candle(market_, tick_interval=time_interval)
result['latest_candle'] = latest_candle

# trim candles
if (N_start_ind == 0):
    N_candle_display = min(N_max_candle,len(candles['result']))
    candles_result = candles['result'][-N_candle_display:]
elif (N_start_ind>=(len(candles['result'])-N_min_candle)):
    N_candle_display = 0;
    candles_result = []
else:
    N_candle_display = min(N_max_candle,len(candles['result'])-N_start_ind)
    candles_result = candles['result'][(-N_start_ind-N_candle_display):-N_start_ind]

result['N_candle_display'] = N_candle_display;

# get result
date = []
for t in candles_result:
    date_ind = dt.date2num(datetime.strptime(t['T'], '%Y-%m-%dT%H:%M:%S'))
    date.append(date_ind)

closep = [t['C'] for t in candles_result]
highp = [t['H'] for t in candles_result]
lowp = [t['L'] for t in candles_result]
openp = [t['O'] for t in candles_result]
volume = [t['V'] for t in candles_result]


result['date'] = date
result['closep'] = closep
result['highp'] = highp
result['lowp'] = lowp
result['openp'] = openp
result['volume'] = volume


# In[10]:


result


# In[5]:


from get_info_from_bittrex_py import getCandleFromBittrex

coin_base = "USDT"
coin_exchange = "OMG"
market_ = coin_base + "-" + coin_exchange
print market_
time_interval = "oneMin"
N_start_ind = 1;
N_max_candle = 200;
N_min_candle = 10;

getCandleFromBittrex(coin_base, coin_exchange, market_, time_interval, N_start_ind, N_max_candle, N_min_candle)

