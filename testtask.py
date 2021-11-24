import ccxt 
#from models import Coin 
#from celery import shared_task
#from channels.layers import get_channel_layer
#from asgiref.sync import async_to_sync


list_unit = ['BTC/USDT','ETH/USDT', 'ADA/USDT', 'BNB/USDT', 'XRP/USDT','SOL/USDT', 'XRP/USDT','DOT/USDT','USDC/USDT','SHIB/USDT','LUNA/USDT','UNI/USDT','AVAX/USDT','LINK/USDT',
'LTC/USDT','BUSD/USDT','BCH/USDT','ALGO/USDT','MATIC/USDT','XLM/USDT','VET/USDT','ATOM/USDT','ICP/USDT','ICP/USDT','AXS/USDT', 'FTT/USDT','FIL/USDT','FTM/USDT','TRX/USDT','ETC/USDT']

exchange = ccxt.binance()
for cointype in list_unit:
    # if(unit_of_currency) in market:
    data = exchange.fetchOHLCV(symbol=cointype,timeframe='1m',since=None, limit=1)
    for candles in data:
        #obj =  Coin.objects.create(typeCoin=market, value=candles[4])
        print(cointype, candles[4])



# unit_of_currency = 'USDT'          #'BTC/USDT','ETH/USDT', 'BNB/USDT', 


# markets = exchange.load_markets()
# count = 0
# for market in markets:
#     if unit_of_currency in market:
#         count = count + 1
#         print(market)
# print(count)