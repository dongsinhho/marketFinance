import ccxt
from .models import Coin 
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.forms.models import model_to_dict

channel_layer = get_channel_layer()

@shared_task
def get_coins_data():
    data_send = []
    unit_of_currency = 'USDT'
    exchange = ccxt.idex()
    markets = exchange.load_markets()
    for market in markets:
        if unit_of_currency in market:
            sample = exchange.fetchOHLCV(symbol=market,timeframe='1m',since=None, limit=1)
            for candles in sample:
                obj =  Coin.objects.create(typeCoin=market, value=candles[4])
                obj_data = model_to_dict(obj)
                data_send.append(obj_data)
                
    async_to_sync(channel_layer.group_send)('Coin', {'type': 'send_new_data', 'text': data_send})



# Kiem tra va chon 50 cointype tu` api va gui ve cho client

