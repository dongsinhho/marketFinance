import ccxt
from .models import Coin 
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.forms.models import model_to_dict

channel_layer = get_channel_layer()

@shared_task
def get_coins_data():
    list_unit = ['BTC/USDT','ETH/USDT', 'ADA/USDT', 'BNB/USDT', 'XRP/USDT','SOL/USDT', 'XRP/USDT','DOT/USDT','USDC/USDT','SHIB/USDT','LUNA/USDT','UNI/USDT','AVAX/USDT','LINK/USDT',
'LTC/USDT','BUSD/USDT','BCH/USDT','ALGO/USDT','MATIC/USDT','XLM/USDT','VET/USDT','ATOM/USDT','ICP/USDT','ICP/USDT','AXS/USDT', 'FTT/USDT','FIL/USDT','FTM/USDT','TRX/USDT','ETC/USDT']
    data_send = []
    #unit_of_currency = 'USDT'
    exchange = ccxt.binance()
    for market in list_unit:
            sample = exchange.fetchOHLCV(symbol=market,timeframe='1m',since=None, limit=1)
            for candles in sample:
                obj =  Coin.objects.create(typeCoin=market, value=candles[4])
                obj_data = model_to_dict(obj)
                data_send.append(obj_data)
                
    async_to_sync(channel_layer.group_send)('Coin', {'type': 'send_new_data', 'text': data_send})



# Kiem tra va chon 50 cointype tu` api va gui ve cho client

