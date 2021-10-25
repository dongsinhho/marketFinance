import ccxt 
#from models import Coin 
#from celery import shared_task
#from channels.layers import get_channel_layer
#from asgiref.sync import async_to_sync



#def get_coins_data():
unit_of_currency = 'USDT'          #'BTC/USDT','ETH/USDT', 'BNB/USDT', 
exchange = ccxt.idex()
markets = exchange.load_markets()
count = 0
for market in markets:
    if unit_of_currency in market:
        count = count + 1
        print(market)
print(count)
# for market in markets:
#     if(unit_of_currency) in market:
#         data = exchange.fetchOHLCV(symbol=market,timeframe='1m',since=None, limit=1)
#         for candles in data:
#             #obj =  Coin.objects.create(typeCoin=market, value=candles[4])
#             print(market)






