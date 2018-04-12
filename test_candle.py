
# coding: utf-8

# In[1]:


get_ipython().magic(u'matplotlib inline')

import matplotlib.pyplot as plt
import matplotlib.finance as mticker
from matplotlib.finance import candlestick_ochl
import matplotlib.dates as dt
from datetime import datetime
import matplotlib.ticker as mticker


from plot_candle_and_volume_py import plot_candle



import numpy
keys = dict()
secrets = dict()


# In[3]:


from bittrex.bittrex import Bittrex, API_V1_1, API_V2_0

keys['bittrex'] = ''
secrets['bittrex'] = ''

marketPlatform = "bittrex"
API_V20 = Bittrex(keys[marketPlatform], secrets[marketPlatform], api_version=API_V2_0)
API_V11 = Bittrex(keys[marketPlatform], secrets[marketPlatform], api_version=API_V1_1)


# In[20]:


market_ = "USDT-OMG"
print(API_V20.get_latest_candle(market=market_,tick_interval="Day"))
print(API_V11.get_marketsummary(market_))
print(market_)


# In[21]:


a=API_V11.get_marketsummary(market_)


# In[25]:


a['result'][0]['TimeStamp']


# In[26]:


candle_result


# In[ ]:


# bittrex
marketPlatform = "bittrex"

from bittrex.bittrex import Bittrex, API_V1_1, API_V2_0
from bittrex.bittrex import BUY_ORDERBOOK, SELL_ORDERBOOK, BOTH_ORDERBOOK
from bittrex.bittrex import TICKINTERVAL_ONEMIN, TICKINTERVAL_FIVEMIN, TICKINTERVAL_THIRTYMIN
from bittrex.bittrex import TICKINTERVAL_HOUR, TICKINTERVAL_DAY

API_V20 = Bittrex('','',api_version=API_V2_0)
API_V11 = Bittrex('','',api_version=API_V1_1)
# get candle, generate ohlc
candles = API_V20.get_candles(market_, tick_interval=time_interval)
lasest_candle = API_V20.get_latest_candle(market_, tick_interval=time_interval)
N_candle_display = min(200,len(candles['result']))
candles_result = candles['result'][-N_candle_display:]

date = []
for t in candles_result:
    date_ind = dt.date2num(datetime.strptime(t['T'], '%Y-%m-%dT%H:%M:%S'))
    date.append(date_ind)
    
closep = [t['C'] for t in candles_result]
highp = [t['H'] for t in candles_result]
lowp = [t['L'] for t in candles_result]
openp = [t['O'] for t in candles_result]
volume = [t['V'] for t in candles_result]


# In[30]:



market_summary = API_V11.get_marketsummary(market_)
result['current_time'] = datetime.strptime(market_summary['result'][0]['TimeStamp'], '%Y-%m-%dT%H:%M:%S')


# In[35]:


datetime.strptime(market_summary['result'][0]['TimeStamp'], '%Y-%m-%dT%H:%M:%S.%f')


# In[ ]:


plot_candle(date, openp, closep, highp, lowp, volume,
               time_interval, marketPlatform, coin_base, coin_exchange)

