
# coding: utf-8

# In[ ]:


from stock_index_functions import get_ema
def process_candle_result(candle_result):
    date=candle_result['date']
    closep=candle_result['closep']
    openp = candle_result['openp']
    highp = candle_result['highp']
    lowp = candle_result['lowp']
    volume = candle_result['volume']
    book_volume = candle_result['book_volume']
    last_trade_price = candle_result['current_price']
    last_trade_time = candle_result['current_time']

    close_ema_7 = get_ema(closep, 7)
    close_ema_14 = get_ema(closep, 14)
    close_ema_30 = get_ema(closep, 30)
    close_ema_60 = get_ema(closep, 60)
    
    last_trade_price_to_current_ema_7 = (last_trade_price - close_ema_7[-1])/close_ema_7[-1]
    last_trade_price_to_current_ema_14 = (last_trade_price - close_ema_14[-1])/close_ema_14[-1]
    last_trade_price_to_current_ema_30 = (last_trade_price - close_ema_30[-1])/close_ema_30[-1]
    last_trade_price_to_current_ema_60 = (last_trade_price - close_ema_60[-1])/close_ema_60[-1]
    
    diff_14_30 = [];
    for i in range (0,len(closep)):
        diff_14_30.append(close_ema_14[i]-close_ema_30[i])

    dea_14_30_10 = get_ema(diff_14_30, 10)
    bar_diff_14_30_dea_10 = []
    bar_diff_14_30_dea_10.append(0)
    for i in range (1,len(closep)):
        bar_diff_14_30_dea_10.append(diff_14_30[i]-dea_14_30_10[i])

    
    
    volume_ema_7 = get_ema(volume, 7)
    volume_ema_14 = get_ema(volume, 14)
    volume_ema_30 = get_ema(volume, 30)
    volume_ema_60 = get_ema(volume, 60)
    result = dict()
    result['close_ema_7'] = close_ema_7
    result['close_ema_14'] = close_ema_14
    result['close_ema_30'] = close_ema_30
    result['close_ema_60'] = close_ema_60

    result['volume_ema_7'] = volume_ema_7
    result['volume_ema_14'] = volume_ema_14
    result['volume_ema_30'] = volume_ema_30
    result['volume_ema_60'] = volume_ema_60
    
    result['last_trade_price_to_current_ema_7'] = last_trade_price_to_current_ema_7
    result['last_trade_price_to_current_ema_14'] = last_trade_price_to_current_ema_14
    result['last_trade_price_to_current_ema_30'] = last_trade_price_to_current_ema_30
    result['last_trade_price_to_current_ema_60'] = last_trade_price_to_current_ema_60
    result['diff_14_30'] = diff_14_30
    result['dea_14_30_10'] = dea_14_30_10
    result['bar_diff_14_30_dea_10'] = bar_diff_14_30_dea_10
    
    return result


# In[ ]:


from get_info_from_bittrex_py import getCandleFromBittrex
candle_result = getCandleFromBittrex("USDT-OMG", time_interval='Day')



import matplotlib.pyplot as plt
import matplotlib.finance as mticker
from matplotlib.finance import candlestick_ochl
import matplotlib.dates as dt
plt.rcParams['figure.figsize'] = [18,10]
#def display_candle_volume_macd(candle_result)
if 1:
    N_candle_display_max=200
    
    
    processed_candle_result = process_candle_result(candle_result)
    if(candle_result['time_interval']=='oneMin'):
        width1 = 0.0005
        width2 = 0.0015
    if(candle_result['time_interval']=='fiveMin'):
        width1 = 0.0003
        width2 = 0.0010
    if(candle_result['time_interval']=='thirtyMin'):
        width1 = 0.0003
        width2 = 0.01
    if(candle_result['time_interval']=='Hour'):
        width1 = 0.0003
        width2 = 0.01
    if(candle_result['time_interval']=='Day'):
        width1 = 0.003
        width2 = 0.1
    
    N_candle_display = min(N_candle_display_max,len(candle_result['date']))
    date=candle_result['date'][-N_candle_display:]
    closep=candle_result['closep'][-N_candle_display:]
    openp = candle_result['openp'][-N_candle_display:]
    highp = candle_result['highp'][-N_candle_display:]
    lowp = candle_result['lowp'][-N_candle_display:]
    volume = candle_result['volume'][-N_candle_display:]
    book_volume = candle_result['book_volume'][-N_candle_display:]
    
    close_ema_7 = processed_candle_result['close_ema_7'][-N_candle_display:]
    close_ema_14 = processed_candle_result['close_ema_14'][-N_candle_display:]
    close_ema_30 = processed_candle_result['close_ema_30'][-N_candle_display:]
    close_ema_60 = processed_candle_result['close_ema_60'][-N_candle_display:]
    
    volume_ema_7 = processed_candle_result['volume_ema_7'][-N_candle_display:]
    volume_ema_14 = processed_candle_result['volume_ema_14'][-N_candle_display:]
    volume_ema_30 = processed_candle_result['volume_ema_30'][-N_candle_display:]
    volume_ema_60 = processed_candle_result['volume_ema_60'][-N_candle_display:]

    diff_14_30 = processed_candle_result['diff_14_30'][-N_candle_display:]
    dea_14_30_10 = processed_candle_result['dea_14_30_10'][-N_candle_display:]
    bar_diff_14_30_dea_10 = processed_candle_result['bar_diff_14_30_dea_10'][-N_candle_display:]

    current_date = dt.date2num(candle_result['current_time'])
    current_price = candle_result['current_price']
    
    ohlc = []
    for i in range (0,len(closep)):
        append_me = date[i], openp[i], closep[i], highp[i], lowp[i], volume[i]
        ohlc.append(append_me)
    
    fig1, ax1 = plt.subplots()
    # price
    c=candlestick_ochl(ax1, ohlc, width=width1, colorup='#77d879', colordown='#db3f3f')
    
    l1, = plt.plot(date, close_ema_7, 'r-', label="ema_7")
    l2, = plt.plot(date,close_ema_14, 'g-', label="ema_14")
    l3, = plt.plot(date,close_ema_30, 'b-', label="ema_30")
    l4, = plt.plot(date,close_ema_60, 'k-', label="ema_60")
    plt.plot([current_date,date[0]],[current_price,current_price],"y--")
    ax1.set_ylim([min(lowp)-2*(max(highp)-min(lowp)), max(highp)])

    # volume
    ax2 = ax1.twinx()

    volume_up = [];
    date_up = [];
    volume_down = [];
    date_down = [];

    for i in range (0,len(closep)):
        if (openp[i]<closep[i]):
            volume_up.append(volume[i])
            date_up.append(date[i])
        else:
            volume_down.append(volume[i])
            date_down.append(date[i])
    plt.bar(date_up, volume_up, width2, color = 'g')
    plt.bar(date_down, volume_down, width2, color = 'r')
    plt.plot(date, volume_ema_7, 'r-')
    plt.plot(date, volume_ema_14, 'g-')
    plt.plot(date, volume_ema_30, 'b-')
    plt.plot(date, volume_ema_60, 'k-')
    ax2.set_ylim([min(volume)-1*(max(volume)-min(volume)), max(volume)+1*(max(volume)-min(volume))])
    
#    ax2.set_ylim([min(volume)-3*(max(volume)-min(volume)), max(volume)+2*(max(volume)-min(volume))])
#    ax3 = ax1.twinx()
#    plt.bar(date,book_volume,0.2)
#    ax3.set_ylim([min(book_volume)-2*(max(book_volume)-min(book_volume)), max(book_volume)+3*(max(book_volume)-min(book_volume))])

# macd

    bar_diff_dea_9_up = [];
    date_up = [];
    bar_diff_dea_9_down = [];
    date_down = [];

    for i in range (0,len(closep)):
        if (bar_diff_14_30_dea_10[i]>0):
            bar_diff_dea_9_up.append(bar_diff_14_30_dea_10[i])
            date_up.append(date[i])
        else:
            bar_diff_dea_9_down.append(bar_diff_14_30_dea_10[i])
            date_down.append(date[i])

    ax4 = ax1.twinx()
    plt.bar(date_up, bar_diff_dea_9_up, width2, color = 'g')
    plt.bar(date_down, bar_diff_dea_9_down, width2, color = 'r')
    l5, = plt.plot(date,diff_14_30, 'b', label = "diff_14_30")
    l6, = plt.plot(date,dea_14_30_10,'r', label =  "dea_10")


    ax4.xaxis.label.set_color('red')
    ax4.tick_params(axis='y', colors='red')

    ax4.set_ylim([min(diff_14_30)-0*(max(diff_14_30)-min(diff_14_30)), max(diff_14_30)+2*(max(diff_14_30)-min(diff_14_30))])

    plt.legend(handles = [l1,l2,l3,l4,l5,l6], loc = 3)
    ax4.xaxis.set_major_formatter(dt.DateFormatter('%dT%H:%M'))





    plt_title = candle_result['marketPlatform'] + ': ' + candle_result['market_']
    plt_title += ', N_candle=' + str(N_candle_display)
    plt_title += ', time_interval=' + candle_result['time_interval']
    plt_title += '\n'+ candle_result['market_summary']['result'][0]['TimeStamp']
    plt_title += ', current_price=' + str(candle_result['market_summary']['result'][0]['Last'])
    plt_title += '\nOpen_Buy/Sell_Order=' + str(candle_result['market_summary']['result'][0]['OpenBuyOrders'])    
    plt_title += '/' + str(candle_result['market_summary']['result'][0]['OpenSellOrders'])    
    plt_title += '\n current_price_above_ema7/14/30/60 in%='
    plt_title += "{:.1f}".format(100*processed_candle_result['last_trade_price_to_current_ema_7'])
    plt_title += "{:.1f}".format(100*processed_candle_result['last_trade_price_to_current_ema_14'])
    plt_title += "{:.1f}".format(100*processed_candle_result['last_trade_price_to_current_ema_30'])
    plt_title += "{:.1f}".format(100*processed_candle_result['last_trade_price_to_current_ema_60'])
    plt.title(plt_title)

    plt.show()

print("done")


# In[1]:


from get_info_from_bittrex_py import getCandleFromBittrex
from stock_index_functions import process_candle_result

candle_result = getCandleFromBittrex("USDT-OMG", time_interval="FiveMin")
processed_candle_result = process_candle_result(candle_result)


# In[ ]:


"{:.2f}".format(100*processed_candle_result['last_trade_price_to_current_ema_7'])


# In[ ]:


# scan all
from get_info_from_bittrex_py import getCandleFromBittrex
from bittrex.bittrex import Bittrex, API_V1_1, API_V2_0

API_V20 = Bittrex('','',api_version=API_V2_0)
API_V11 = Bittrex('','',api_version=API_V1_1)

market_sum = API_V20.get_market_summaries()
market_list = market_sum['result']
for t in market_list:
    market_=t['Market']['MarketName']
    
    
print('done')

