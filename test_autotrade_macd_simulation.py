
# coding: utf-8

# In[35]:


from get_info_from_bittrex_py import getCandleFromBittrex
from stock_index_functions import process_candle_result, display_candle_volume_macd

candle_result = getCandleFromBittrex("USDT-OMG", time_interval="oneMin")
processed_candle_result = process_candle_result(candle_result)
fig1=display_candle_volume_macd(candle_result)


# In[34]:


closep = candle_result['closep']
one_trade_max_profit = max(closep)/min(closep)-1

activity_list = autotrade_simulator(candle_result, processed_candle_result, method="macd_cross")
macd_profit = activity_list[-1]['money'] + closep[-1]*activity_list[-1]['coin'] -1
print(macd_profit)
print(macd_profit/one_trade_max_profit)

rand_profit=[]
for i in range(1,100):
    activity_list = autotrade_simulator(candle_result, processed_candle_result, method="rand")
    rand_profit.append(activity_list[-1]['money'] + closep[-1]*activity_list[-1]['coin'] -1)
print(max(rand_profit))


# In[25]:


max(rand_profit)


# In[ ]:


buy_point_list = [];
sell_point_list = [];
for i in range (62,len(processed_candle_result['bar_diff_14_30_dea_10'])):
    diff_privious = processed_candle_result['bar_diff_14_30_dea_10'][i-1]
    diff_current = processed_candle_result['bar_diff_14_30_dea_10'][i]
    if (diff_privious>0) and (diff_current<0):
        sell_point = dict()
        sell_point['date']=candle_result['date'][i]
        sell_point['price']=candle_result['closep'][i]
        sell_point_list.append(sell_point)
    if (diff_privious<0) and (diff_current>0):
        buy_point = dict()
        buy_point['date']=candle_result['date'][i]
        buy_point['price']=candle_result['closep'][i]
        buy_point_list.append(buy_point)
        
        
        
        


# In[ ]:


import random
sell_trigger = random.random()>0.5
print(sell_trigger)


# In[10]:


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
    buy_trigger = buy_trigger and current_price<previous_activity_price*fee_rate
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



# In[18]:





# In[ ]:


activity_list[-1]['money']+activity_list[-1]['money']

activity_list = autotrade_simulator(candle_result, processed_candle_result, method="macd_cross")
closep = candle_result['closep']
one_trade_max_profit = max(closep)/min(closep)*money


# In[ ]:


activity_list


# In[13]:


import matplotlib.pyplot as plt
import matplotlib.finance as mticker
from matplotlib.finance import candlestick_ochl
import matplotlib.dates as dt
plt.rcParams['figure.figsize'] = [18,10]
closep = candle_result['closep']
date = candle_result['date']
diff = processed_candle_result['diff_14_30']
dea = processed_candle_result['dea_14_30_10']

buy_date = [t['date'] for t in buy_point_list]
buy_price = [t['price'] for t in buy_point_list]
sell_date = [t['date'] for t in sell_point_list]
sell_price = [t['price'] for t in sell_point_list]

fig2, ax1 = plt.subplots()
l1, = plt.plot(buy_date, buy_price, 'ro', label = 'buy_point')
l2, = plt.plot(sell_date, sell_price, 'bo', label = 'sell_point')
plt.plot(date,closep)

ax2 = ax1.twinx()
plt.plot(date,diff,'b')
plt.plot(date,dea,'r')

activity_date = [t['date'] for t in activity_list]
activity_value = [t['value'] for t in activity_list]
ax3 = ax1.twinx()
plt.plot(activity_date, activity_value,'g--')

ax3.xaxis.set_major_formatter(dt.DateFormatter('%dT%H:%M'))
plt.legend(handles = [l1,l2], loc = 4)
plt.show()



# In[14]:


activity_list


# In[ ]:


13.38001517*0.99

