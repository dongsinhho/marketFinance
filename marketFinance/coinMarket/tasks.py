import ccxt
from .models import Coin 
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def get_coins_data():
    unit_of_currency = 'USDT'
    exchange = ccxt.binance()
    markets = exchange.load_markets()
    for market in markets:
        if(unit_of_currency) in market:
            data = exchange.fetchOHLCV(symbol=market,timeframe='1m',since=None, limit=1)
            for candles in data:
                obj =  Coin.objects.create(typeCoin=market, value=candles[4])
                print("test success")






