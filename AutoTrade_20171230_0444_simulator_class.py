
# coding: utf-8

# In[1]:


def find_buy_point_in_all_markets(public_api, markets_list, time_interval, N_candle = 200, method = 'macd_cross'):
    for market_ in markets_list:
        bs_point = find_buy_sell_point(public_api, market_, time_interval)
        if bs_point['b_macd_buy'] == True:
            print('a buy point is just identified among the markets list.')
            print(bs_point)
            return bs_point
    buy_point = dict()
    buy_point['b_macd_buy'] = False
    return buy_point
    


# In[2]:


def find_buy_sell_point(public_api, market_, time_interval, N_candle = 200, method = 'macd_cross'):
    from get_info_from_bittrex_py import getCandleFromBittrex
    import matplotlib.dates as dt
    from stock_index_functions import process_candle_result_with_current_price

    API_V20 = public_api['API_V20']
    API_V11 = public_api['API_V11']
    
    bs_point = dict()
    bs_point['market_'] = market_
    bs_point['time_interval'] = time_interval
    bs_point['method'] = method
    candle_result = getCandleFromBittrex(market_, time_interval, N_max_candle=N_candle)
    # get info error
    if not(candle_result.has_key('N_candle_stored')):
        bs_point['b_macd_buy'] = False
        bs_point['b_macd_sell'] = False
        bs_point['info'] = 'error candle result'
        return bs_point
    if candle_result['N_candle_stored']<N_candle:
        bs_point['b_macd_buy'] = False
        bs_point['b_macd_sell'] = False
        bs_point['info'] = 'not enough candles'
        return bs_point

    if method == 'macd_cross':
        # last trade happen at last candle, cannot callulate macd
        if dt.date2num(candle_result['current_time'])<candle_result['date'][-1]:
            bs_point['b_macd_buy'] = False
            bs_point['b_macd_sell'] = False
            bs_point['info'] = 'not enough candles'
            return bs_point
            
        processed_candle_result_with_current_price = process_candle_result_with_current_price(candle_result)
        
        diff_current = processed_candle_result_with_current_price['bar_diff_14_30_dea_10'][-1]
        diff_previous = processed_candle_result_with_current_price['bar_diff_14_30_dea_10'][-2]

        # not a mcad buy point
        if diff_current*diff_previous>=0:
            bs_point['b_macd_buy'] = False
            bs_point['b_macd_sell'] = False
            bs_point['info'] = 'not a mcad point'
            return bs_point
        
        if diff_current<0:
            bs_point['b_macd_buy'] = False
            bs_point['b_macd_sell'] = True
            bs_point['info'] = 'mcad sell point'
        if diff_current>0:
            bs_point['b_macd_buy'] = True
            bs_point['b_macd_sell'] = False
            bs_point['info'] = 'mcad buy point'

#         #####
#         bs_point['b_macd_buy'] = True
        
        
        bs_point['BuyOrder'] = candle_result['market_summary']['result'][0]['OpenBuyOrders']
        bs_point['SellOrder'] = candle_result['market_summary']['result'][0]['OpenSellOrders']
        bs_point['BuySellRatio'] = float(bs_point['BuyOrder'])/bs_point['SellOrder']
        bs_point['BaseVolume'] = candle_result['market_summary']['result'][0]['BaseVolume']
        bs_point['current_ask'] = candle_result['market_summary']['result'][0]['Ask']
        bs_point['current_bid'] = candle_result['market_summary']['result'][0]['Bid']
        bs_point['current_high'] = candle_result['market_summary']['result'][0]['High']
        bs_point['current_low'] = candle_result['market_summary']['result'][0]['Low']
        bs_point['current_time'] = candle_result['current_time']
        bs_point['current_price'] = candle_result['current_price']
        bs_point['last_trade_price_to_current_ema_7'] = processed_candle_result_with_current_price['last_trade_price_to_current_ema_7']
        bs_point['last_trade_price_to_current_ema_14'] = processed_candle_result_with_current_price['last_trade_price_to_current_ema_14']
        bs_point['last_trade_price_to_current_ema_30'] = processed_candle_result_with_current_price['last_trade_price_to_current_ema_30']
        bs_point['last_trade_price_to_current_ema_60'] = processed_candle_result_with_current_price['last_trade_price_to_current_ema_60']
        bs_point['current_volume_ema_7'] = processed_candle_result_with_current_price['volume_ema_7'][-1]
        bs_point['current_volume_ema_14'] = processed_candle_result_with_current_price['volume_ema_14'][-1]
        bs_point['current_volume_ema_30'] = processed_candle_result_with_current_price['volume_ema_30'][-1]
        bs_point['current_volume_ema_60'] = processed_candle_result_with_current_price['volume_ema_60'][-1]
        bs_point['diff_current'] = diff_current
        bs_point['diff_previous'] = diff_previous
        return bs_point
        


# In[3]:


class Simulator:

#    coin_base
#    coin_exchage_list
#    market_list
    
#    current_price_list
#    bought_price_list
#    buying_price_list
#    selling_price_list

#    pending_buying_amount_list
#    pending_selling_amount_list
#    amount_exchange_list
    
#    available_amount_base
#    pending_amount_base
    
#    wallet_value
    
#    public_api
#    private_api
    
    def __init__(self, coin_base, coin_exchange_list, private_key, private_secret):
        from bittrex.bittrex import Bittrex, API_V1_1, API_V2_0
        self.public_api = dict()
        self.public_api['API_V20'] = Bittrex('','',api_version=API_V2_0)
        self.public_api['API_V11'] = Bittrex('','',api_version=API_V1_1)
        self.private_api = dict()
        self.private_api['API_V20'] = Bittrex(private_key,private_secret,api_version=API_V2_0)
        self.private_api['API_V11'] = Bittrex(private_key,private_secret,api_version=API_V1_1)

        self.coin_base = coin_base
        self.coin_exchange_list= coin_exchange_list
        self.market_list = []
        self.current_price_list = dict()
        self.bought_price_list = dict()
        self.buying_price_list = dict()
        self.selling_price_list = dict()
        self.pending_buy_amount_list = dict()
        self.pending_sell_amount_list = dict()
        self.amount_exchange_list = dict()
        self.base_volume_list = dict()
        
        for coin_exchange_ in self.coin_exchange_list:
            market_ = coin_base + '-' + coin_exchange_
            self.market_list.append(market_)
            self.current_price_list[market_] = 0
            self.base_volume_list[market_] = 0
            self.bought_price_list[market_] = 0
            self.buying_price_list[market_] = 0
            self.selling_price_list[market_] = 999999.99999
            self.pending_buy_amount_list[coin_exchange_] = 0
            self.pending_sell_amount_list[coin_exchange_] = 0
            self.amount_exchange_list[coin_exchange_] = 0
    
        self.available_amount_base = 0
        self.pending_amount_base = 0

        self.wallet_value = 0
        
    def update_one_market_price(self, market_):
        t_result = self.public_api['API_V11'].get_marketsummary(market_)
        self.current_price_list[market_] = t_result['result'][0]['Last']
        self.base_volume_list[market_] = t_result['result'][0]['BaseVolume']
        return self.current_price_list[market_]
    
#     def update_one_coin_status(self, coin_exchange_):
#         market_ = self.coin_base + '-' + coin_exchange_
#         self.update_one_market_price(market_)
#         pending_buy_amount = self.pending_buy_amount_list[coin_exchange_]
#         pending_sell_amount = self.pending_sell_amount_list[coin_exchange_]
#         current_price = self.current_price_list[market_]
#         if pending_buy_amount>0:
#             buying_price = self.buying_price_list[market_]
#             if current_price<buying_price:
#                 self.pending_amount_base = self.pending_amount_base - pending_buy_amount*buying_price
#                 self.amount_exchange_list[coin_exchange_] = pending_buy_amount*0.99
#                 self.pending_buy_amount_list[coin_exchange_] = 0
#                 self.bought_price_list[market_] = self.buying_price_list[market_]
#                 self.buying_price_list[market_] = 0

#         if pending_sell_amount>0:
#             selling_price = self.selling_price_list[market_]
#             if current_price>selling_price:
#                 self.available_amount_base = self.available_amount_base + pending_sell_amount*selling_price*0.99
#                 self.pending_sell_amount_list[coin_exchange_] = 0
#                 self.selling_price_list[market_] = 999999.99999
        
        
    
    def update_account(self):

        #get_coin_base_wallet
        
        for coin_exchange_ in self.coin_exchange_list:
#            get_coin_exchange_wallet(self, coin_exchange_)
            market_ = self.coin_base + '-' + coin_exchange_
            self.update_one_market_price(market_)
        
            # the following is only for simulator
            pending_buy_amount = self.pending_buy_amount_list[coin_exchange_]
            pending_sell_amount = self.pending_sell_amount_list[coin_exchange_]
            current_price = self.current_price_list[market_]
            if pending_buy_amount>0:
                buying_price = self.buying_price_list[market_]
                if current_price<buying_price:
                    self.pending_amount_base = self.pending_amount_base - pending_buy_amount*buying_price
                    self.amount_exchange_list[coin_exchange_] = pending_buy_amount*0.99
                    self.pending_buy_amount_list[coin_exchange_] = 0
                    self.bought_price_list[market_] = self.buying_price_list[market_]
                    self.buying_price_list[market_] = 0
            
            if pending_sell_amount>0:
                selling_price = self.selling_price_list[market_]
                if current_price>selling_price:
                    self.available_amount_base = self.available_amount_base + pending_sell_amount*selling_price*0.99
                    self.pending_sell_amount_list[coin_exchange_] = 0
                    self.selling_price_list[market_] = 999999.99999

        self.wallet_value = self.available_amount_base + self.pending_amount_base
        for coin_exchange_ in self.coin_exchange_list:
            market_ = self.coin_base + '-' + coin_exchange_
            pending_amount = self.pending_sell_amount_list[coin_exchange_]
            avail_amount = self.amount_exchange_list[coin_exchange_] 
            current_price = self.current_price_list[market_]   
            owing_amount = pending_amount + avail_amount
            
            self.wallet_value += owing_amount * current_price
            
            
    def display_account(self):
        text = 'wallet_value = '+"{0:.5f}".format(self.wallet_value)
        text += '\n'+ self.coin_base + '  avail = ' + "{0:.5f}".format(self.available_amount_base)
        text += ' ,pdng = {0:.5f}'.format(self.pending_amount_base)
        print(text)
        print('coin      avail    pdng_buy   pdng_sell   price         base_Volume   recent_buy_price    buying_price   selling_price')
        for coin_exchange_ in self.coin_exchange_list:
            market_ = self.coin_base + '-' + coin_exchange_
            current_price = self.current_price_list[market_]
            recent_buy_price = self.bought_price_list[market_]
            pdng_buy = self.pending_buy_amount_list[coin_exchange_]
            pdng_sell = self.pending_sell_amount_list[coin_exchange_]
            avail = self.amount_exchange_list[coin_exchange_]
            buying_price = self.buying_price_list[market_]
            selling_price = self.selling_price_list[market_]
            base_volume = self.base_volume_list[market_]

            text = "{:5}".format(coin_exchange_) + '    ' + "{0:.5f}".format(avail) + '   '
            text += "{0:.5f}".format(pdng_buy)+'     '+"{0:.5f}".format(pdng_sell)+' '
            text += "{0:012.5f}".format(current_price)+'   '+"{0:012.0f}".format(base_volume)+'    '
            text += "{0:012.5f}".format(recent_buy_price)+'      '
            text += "{0:012.5f}".format(buying_price)+'   '+"{0:012.5f}".format(selling_price)
            print(text)
        
    def set_buy_order(self, coin_base, coin_exchange_, price, amount):
        market_ = coin_base+'-'+coin_exchange_
        
        self.pending_buy_amount_list[coin_exchange_] += amount
        self.buying_price_list[market_] = price
        self.available_amount_base += -amount*price
        self.pending_amount_base += amount*price
        info = dict()
        info['activity'] = 'set_buy'
        info['coin_base'] = coin_base
        info['coin_exchange_'] = coin_exchange_
        info['amount'] = amount
        info['price'] = price
        return info
        
    def set_sell_order(self, coin_base, coin_exchange_, price):

        market_ = coin_base+'-'+coin_exchange_
        amount = self.amount_exchange_list[coin_exchange_]
        
        self.amount_exchange_list[coin_exchange_] = 0
        self.pending_sell_amount_list[coin_exchange_] = amount
        self.selling_price_list[market_] = price

        info = dict()
        info['activity'] = 'set_sell'
        info['coin_base'] = coin_base
        info['coin_exchange_'] = coin_exchange_
        info['amount'] = amount
        info['price'] = price
        return info
    
    def cancel_buy_order(self, coin_base, coin_exchange_):

        market_ = coin_base+'-'+coin_exchange_

        amount = self.pending_buy_amount_list[coin_exchange_]
        price = self.buying_price_list[market_]
        
        self.pending_buy_amount_list[coin_exchange_] = 0
        self.buying_price_list[market_] = 0
        self.available_amount_base += amount*price
        self.pending_amount_base += -amount*price
        
        info = dict()
        info['activity'] = 'cancel_buy'
        info['coin_base'] = coin_base
        info['coin_exchange_'] = coin_exchange_
        info['amount'] = amount
        info['price'] = price
        return info


    def cancel_sell_order(self, coin_base, coin_exchange_):
        
        market_ = coin_base+'-'+coin_exchange_

        amount = self.pending_sell_amount_list[coin_exchange_]
        price = self.selling_price_list[market_]
        
        self.amount_exchange_list[coin_exchange_] = amount
        self.pending_sell_amount_list[coin_exchange_] = 0
        self.selling_price_list[market_] = 999999.99999

        info = dict()
        info['activity'] = 'cancel_sell'
        info['coin_base'] = coin_base
        info['coin_exchange_'] = coin_exchange_
        info['amount'] = amount
        info['price'] = price
        return info
        
        
    
    def get_coin_base_wallet(self):
        # return same amount for simulator
        # for real market use private_api
#        private_api.get_wallet_summary(coin_base)
#        available_amount_base
#        pending_amount_base
        result = dict()
        result['available'] = self.available_amount_base
        result['pending'] = self.pending_amount_base
        return result

    def get_coin_exchange_wallet(self, coin_exchange_):
        # return same amount for simulator
        # for real market use private_api
#        private_api.get_wallet_summary(coin_exchange_)

#        self.amount_exchange_list['coin_exchange'] = 
#        self.pending_buying_amount_list['coin_exchange'] = 
#        self.pending_selling_amount_list['coin_exchange'] = 
        
        result = dict()
        result['available'] = self.amount_exchange_list['coin_exchange']
        result['pending_buy'] = self.pending_buying_amount_list['coin_exchange']
        result['pending_sell'] = self.pending_selling_amount_list['coin_exchange']
        return result
        
    


# In[4]:


# sim = Simulator('USDT', ['ETC','BTC'],'','')
# sim.available_amount_base = 1000
# sim.update_account()  
# sim.display_account()


# In[5]:


coin_base = 'USDT'
time_interval = 'fiveMin'
coin_exchange_list = ['BTC', 'LTC', 'ETC', 'BCC', 'BTG',
                     'DASH', 'ETH', 'NEO', 'OMG', 'XMR', 
                     'XRP', 'ADA', 'XVG', 'NXT','ZEC']
# coin_exchange_list = ['BTC', 'LTC', 'ETC', 'BCC']
market_list = []
for coin_exchange_ in coin_exchange_list:
    market_list.append(coin_base+'-'+coin_exchange_)
    
record_list = []

sim = Simulator(coin_base, coin_exchange_list,'','')
sim.available_amount_base = 1000
sim.update_account()  
sim.display_account()



# In[ ]:


while 1:
    # set buy
    if sim.available_amount_base>0.2*sim.wallet_value:
        buy_point = find_buy_point_in_all_markets(sim.public_api, market_list, time_interval)
        if buy_point['b_macd_buy']:
            coin_exchange_ = buy_point['market_'][(len(sim.coin_base)+1):]
            if (sim.amount_exchange_list[coin_exchange_]+sim.pending_buy_amount_list[coin_exchange_]+sim.pending_sell_amount_list[coin_exchange_])==0:   
                current_price = buy_point['current_price']
#                 amount = sim.available_amount_base*0.3/current_price
                amount = min(sim.available_amount_base*0.8, sim.wallet_value*0.3)/current_price
                info = sim.set_buy_order(sim.coin_base, coin_exchange_, current_price*0.99, amount)
                info['point'] = buy_point
                record_list.append(info)
                sim.display_account()
        
    # cancel buy
    for coin_exchange_ in coin_exchange_list:
        market_ = coin_base+'-'+coin_exchange_
        pending_buy_amount = sim.pending_buy_amount_list[coin_exchange_]
        if pending_buy_amount>0:
            sell_point = find_buy_sell_point(sim.public_api, market_, time_interval)
            if sell_point['b_macd_sell']:
                info = sim.cancel_buy_order(sim.coin_base, coin_exchange_)
                info['point'] = sell_point
                record_list.append(info)
                sim.display_account()
                continue
                
            market_ = coin_base+'-'+coin_exchange_
            buying_price = sim.buying_price_list[market_]
            current_price = sim.current_price_list[market_]
            if buying_price<current_price*0.97:
                info = sim.cancel_buy_order(sim.coin_base, coin_exchange_)
                info['point'] = 'miss the chance to buy'
                record_list.append(info)
                sim.display_account()
                
                

    # set sell
    for coin_exchange_ in sim.coin_exchange_list:
        market_ = coin_base+'-'+coin_exchange_
        avail_coin_exchange = sim.amount_exchange_list[coin_exchange_]
        if avail_coin_exchange>0:
            bought_price = sim.bought_price_list[market_]
            current_price = sim.current_price_list[market_]
            # loss stop
            if current_price < bought_price*0.92:
                info = sim.set_sell_order(sim.coin_base, coin_exchange_, current_price*0.98)
                sim.update_account()  
                info['point'] = 'loss stop'
                record_list.append(info)
                sim.display_account()
                
            
            

            sell_point = find_buy_sell_point(sim.public_api, market_, time_interval)
            if sell_point['b_macd_sell']:
                if current_price > bought_price*1.03:
                    info = sim.set_sell_order(sim.coin_base, coin_exchange_, current_price*0.999)
                    info['point'] = sell_point
                    record_list.append(info)
                    sim.display_account()
    
    # cancel sell
    for coin_exchange_ in coin_exchange_list:
        market_ = coin_base+'-'+coin_exchange_
        pending_sell_amount = sim.pending_sell_amount_list[coin_exchange_]
        if pending_sell_amount>0:
            buy_point = find_buy_sell_point(sim.public_api, market_, time_interval)
            if sell_point['b_macd_buy']:
                info = sim.cancel_sell_order(sim.coin_base, coin_exchange_)
                info['point'] = buy_point
                record_list.append(info)
                sim.display_account()

    sim.update_account()  
    sim.display_account()
        
        
        


# In[12]:


import datetime
for coin_exchange__ in sim.coin_exchange_list:
    for record in record_list:
        text = record['coin_exchange_']
        text += ': ' + record['activity'] + '  ' + str(record['price'])
        if record['point'] == 'loss stop':
            text += '   loss stop'
        else:
            if 'last_trade_price_to_current_ema_7' in record['point']:
                text += "   {0:.3f}".format(100*record['point']['last_trade_price_to_current_ema_7'])
                text += "   {0:.3f}".format(100*record['point']['last_trade_price_to_current_ema_14'])
                text += "   {0:.3f}".format(100*record['point']['last_trade_price_to_current_ema_30'])
                text += "   {0:.3f}".format(100*record['point']['last_trade_price_to_current_ema_60'])
                text += '  ' + record['point']['current_time'].strftime('%H:%M')
        if record['coin_exchange_'] == coin_exchange__:
            print text


# In[ ]:


record_list


# In[ ]:


market_ = coin_base+'-'+coin_exchange_
buying_price = sim.buying_price_list[market_]
current_price = sim.current_price_list[market_]


# In[ ]:


sim.public_api['API_V11'].get_marketsummary(market_)


# In[ ]:



coin_exchange_ = buy_point['market_'][(len(sim.coin_base)+1):]


# In[ ]:


coin_exchange_


# In[ ]:


0.92*0.98


# In[ ]:


record_list


# In[ ]:



    print 'a'


# In[ ]:


buy_set_info = sim.set_buy_order(sim.coin_base, 'ETC', price = 32, amount = 10)
print(buy_set_info)
sim.display_account()
print('%%%%%%%%%%%%%%')

buy_set_info = sim.set_buy_order(sim.coin_base, 'BTC', price = 15000, amount = 0.02)
print(buy_set_info)
sim.display_account()
print('%%%%%%%%%%%%%%%')

sim.update_account()  
sim.display_account()
print('%%%%%%%%%%%%%%%')

buy_cancel_info = sim.cancel_buy_order(sim.coin_base, 'BTC')
print(buy_cancel_info)
sim.display_account()
print('%%%%%%%%%%%%%%%')
print('%%%%%%%%%%%%%%%')
print('%%%%%%%%%%%%%%%')

sell_set_info = sim.set_sell_order(sim.coin_base, 'BTC', price = 15000)
print(sell_set_info)
sim.display_account()
print('%%%%%%%%%%%%%%%')

sell_set_info = sim.set_sell_order(sim.coin_base, 'ETC', price = 31)
print(sell_set_info)
sim.display_account()
print('%%%%%%%%%%%%%%%')

sell_cancel_info = sim.cancel_sell_order(sim.coin_base, 'BTC')
print(sell_cancel_info)
sim.display_account()
print('%%%%%%%%%%%%%%%')
print('%%%%%%%%%%%%%%%')
print('%%%%%%%%%%%%%%%')

sim.update_account()  
sim.display_account()
print('%%%%%%%%%%%%%%%')



# In[ ]:


sim.update_account()  
sim.display_account()
print('%%%%%%%%%%%%%%%')


# In[ ]:


(442574.10514-40)/29.7


# In[ ]:


API_V11=sim.public_api['API_V11']

