
# coding: utf-8

# In[7]:


get_ipython().magic(u'matplotlib inline')

def plot_candle(date, openp, closep, highp, lowp, volume,
               time_interval, coin_base, coin_exchange,
               ):

    import matplotlib.pyplot as plt
    import matplotlib.finance as mticker
    from matplotlib.finance import candlestick_ochl
    import matplotlib.ticker as mticker
    from bittrex.bittrex import TICKINTERVAL_ONEMIN, TICKINTERVAL_FIVEMIN, TICKINTERVAL_THIRTYMIN
    from bittrex.bittrex import TICKINTERVAL_HOUR, TICKINTERVAL_DAY

    market_ = coin_base + "-" + coin_exchange
    # display candle and volume
    x = 0
    y = len(date)
    ohlc = []
    #ax1 = plt.subplot2grid((1,1), (0,0))
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    while x<y:
        append_me = date[x], openp[x], closep[x], highp[x], lowp[x], volume[x]
        ohlc.append(append_me)
        x+=1

    c=candlestick_ochl(ax1, ohlc, width=0.001, colorup='#77d879', colordown='#db3f3f')
    if (time_interval == TICKINTERVAL_DAY):   
        ax1.xaxis.set_major_formatter(dt.DateFormatter('%m-%d'))
    if (time_interval == TICKINTERVAL_HOUR or time_interval == TICKINTERVAL_THIRTYMIN):
        ax1.xaxis.set_major_formatter(dt.DateFormatter('%dT%H'))
    if (time_interval == TICKINTERVAL_ONEMIN or time_interval == TICKINTERVAL_FIVEMIN):   
        ax1.xaxis.set_major_formatter(dt.DateFormatter('%H:%M'))

    ax1.xaxis.set_major_locator(mticker.MaxNLocator(8))
    ax1.set_ylabel(coin_base)
    ax1.set_ylim([min(lowp)-0.5*(max(highp)-min(lowp)), max(highp)])
    ax2.plot(date, volume)
    ax2.set_ylabel('Volume')
    ax2.set_ylim([min(volume), max(volume)+0.7*(max(volume)-min(volume))])
    plt.title(marketPlatform + ': ' + market_ + ', time_interval=' + time_interval)
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0 )
    #plt.savefig(marketPlatform + '_' + market_ + '_' + time_interval, dpi=3000)
    plt.show()




# In[12]:


from bittrex.bittrex import TICKINTERVAL_ONEMIN, TICKINTERVAL_FIVEMIN, TICKINTERVAL_THIRTYMIN
from bittrex.bittrex import TICKINTERVAL_HOUR, TICKINTERVAL_DAY
TICKINTERVAL_HOUR

