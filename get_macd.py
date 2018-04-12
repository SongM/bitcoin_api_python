
# coding: utf-8

# In[ ]:


from stock_index_functions import get_ema

date=candle_result['date']
closep=candle_result['closep']
volume = candle_result['volume']
openp = candle_result['openp']
highp = candle_result['highp']
lowp = candle_result['lowp']


volume_ema_7 = get_ema(volume, 7)
close_ema_7 = get_ema(closep, 7)
volume_ema_14 = get_ema(volume, 14)
close_ema_14 = get_ema(closep, 14)
volume_ema_30 = get_ema(volume, 30)
close_ema_30 = get_ema(closep, 30)
volume_ema_60 = get_ema(volume, 60)
close_ema_60 = get_ema(closep, 60)

fig1, ax1 = plt.subplots()
ohlc = []
for i in range (0,len(closep)):
    append_me = date[i], openp[i], closep[i], highp[i], lowp[i], volume[i]
    ohlc.append(append_me)

c=candlestick_ochl(ax1, ohlc, width=0.002, colorup='#77d879', colordown='#db3f3f')

plt.plot(date,close_ema_7,'r-')
plt.plot(date,close_ema_14,'g-')
plt.plot(date,close_ema_30,'b-')
plt.plot(date,close_ema_60,'k-')
#plt.plot(date,closep,'y--')
ax1.xaxis.set_major_formatter(dt.DateFormatter('%dT%H'))
ax1.set_ylim([min(lowp)-1*(max(highp)-min(lowp)), max(highp)])

# ax2 volume
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
plt.bar(date_up,volume_up,0.02,color = 'g', alpha=0.5)
plt.bar(date_down,volume_down,0.02,color = 'r', alpha=0.5)
plt.plot(date,volume_ema_7,'r-')
plt.plot(date,volume_ema_14,'g-')
plt.plot(date,volume_ema_30,'b-')
plt.plot(date,volume_ema_60,'k-')
ax2.set_ylim([min(volume)-0*(max(volume)-min(volume)), max(volume)+1*(max(volume)-min(volume))])
ax2.xaxis.set_major_formatter(dt.DateFormatter('%dT%H'))


# In[ ]:


ema_12 = get_ema(closep,12)
ema_26 = get_ema(closep,26)
diff = [];
for i in range (0,len(closep)):
    diff.append(ema_12[i]-ema_26[i])

dea_9 = get_ema(diff,9)
bar_diff_dea_9 = []
bar_diff_dea_9.append(0)
for i in range (1,len(closep)):
    bar_diff_dea_9.append(diff[i]-dea_9[i])
    


# In[ ]:


get_ipython().magic(u'matplotlib inline')

import matplotlib.pyplot as plt

import matplotlib.dates as dt

import matplotlib.finance as mticker
from matplotlib.finance import candlestick_ochl
import matplotlib.ticker as mticker

plt.rcParams['figure.figsize'] = [18,8]


# In[ ]:



# ax1 bar
fig1, ax1 = plt.subplots()
ohlc = []
for i in range (0,len(closep)):
    append_me = date[i], openp[i], closep[i], highp[i], lowp[i], volume[i]
    ohlc.append(append_me)

c=candlestick_ochl(ax1, ohlc, width=0.001, colorup='#77d879', colordown='#db3f3f')

plt.plot(date,ema_12,'r-')
plt.plot(date,ema_26,'g-')
#plt.plot(date,closep,'y--')
ax1.xaxis.set_major_formatter(dt.DateFormatter('%dT%H'))
ax1.set_ylim([min(lowp)-2*(max(highp)-min(lowp)), max(highp)])

# ax2 volume
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
plt.bar(date_up,volume_up,0.02,color = 'g')
plt.bar(date_down,volume_down,0.02,color = 'r')
ax2.set_ylim([min(volume)-1*(max(volume)-min(volume)), max(volume)+1*(max(volume)-min(volume))])

# ax3 macd
bar_diff_dea_9_up = [];
date_up = [];
bar_diff_dea_9_down = [];
date_down = [];

for i in range (0,len(closep)):
    if (bar_diff_dea_9[i]>0):
        bar_diff_dea_9_up.append(bar_diff_dea_9[i])
        date_up.append(date[i])
    else:
        bar_diff_dea_9_down.append(bar_diff_dea_9[i])
        date_down.append(date[i])
    
ax3 = ax1.twinx()
plt.bar(date_up,bar_diff_dea_9_up,0.02,color = 'g')
plt.bar(date_down,bar_diff_dea_9_down,0.02,color = 'r')
plt.plot(date,diff,'b')
plt.plot(date,dea_9,'r')

ax3.xaxis.set_major_formatter(dt.DateFormatter('%dT%H'))

ax3.xaxis.label.set_color('red')
ax3.tick_params(axis='y', colors='red')

ax3.set_ylim([min(diff)-0*(max(diff)-min(diff)), max(diff)+2*(max(diff)-min(diff))])



# In[ ]:


[min(diff)-0*(max(diff)-min(diff)), max(diff)+1*(max(diff)-min(diff))]


# In[ ]:


bar_diff_dea_9


# In[ ]:


ema_12[1]


# In[ ]:


closep[1]


# In[ ]:


ema_12[1]*11/13 + closep[2]*2/13-closep[2]


# In[3]:


min(3,4)

