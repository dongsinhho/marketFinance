import ccxt
from .models import Coin, TypeCoin, Notify
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.forms.models import model_to_dict
from django.core.mail import send_mail


channel_layer = get_channel_layer()

@shared_task
def get_coins_data():
    list_unit = []
    typecoins = TypeCoin.objects.all()
    for typecoin in typecoins:
        list_unit.append(model_to_dict(typecoin))
#     list_unit = ['BTC/USDT','ETH/USDT', 'ADA/USDT', 'BNB/USDT', 'XRP/USDT','SOL/USDT', 'XRP/USDT','DOT/USDT','USDC/USDT','SHIB/USDT','LUNA/USDT','UNI/USDT','AVAX/USDT','LINK/USDT',
# 'LTC/USDT','BUSD/USDT','BCH/USDT','ALGO/USDT','MATIC/USDT','XLM/USDT','VET/USDT','ATOM/USDT','ICP/USDT','ICP/USDT','AXS/USDT', 'FTT/USDT','FIL/USDT','FTM/USDT','TRX/USDT','ETC/USDT']
    data_send = []
    #unit_of_currency = 'USDT'
    exchange = ccxt.binance()
    for market in list_unit:
        sample = exchange.fetchOHLCV(symbol=market['name'],timeframe='1m',since=None, limit=1)
        for candles in sample:
            status = False           
            try:
                old_coin = Coin.objects.filter(typeCoin=typecoins[list_unit.index(market)]).order_by('-time').first()
            except:
                old_coin = None
            obj =  Coin.objects.create(typeCoin=typecoins[list_unit.index(market)], value=candles[4])
            if old_coin and old_coin.value < obj.value:
                status = True
            obj_dict = model_to_dict(obj)
            obj_dict.update({'status':status})
            obj_dict.update({'id':market['id']})
            obj_dict.update({'typeCoin':market['name']})
            data_send.append(obj_dict)
                
    async_to_sync(channel_layer.group_send)('Coin', {'type': 'send_new_data', 'text': data_send})

# Tính năng mới: tạo các lớp người dùng khác nhau để chỉ gửi cho họ những coin họ thích

# Kiem tra va chon 50 cointype tu` api va gui ve cho client

# ['BTC/USDT','ETH/USDT', 'ADA/USDT', 'BNB/USDT', 'XRP/USDT','SOL/USDT', 'XRP/USDT','DOT/USDT','USDC/USDT','SHIB/USDT','LUNA/USDT','UNI/USDT','AVAX/USDT','LINK/USDT',
# 'LTC/USDT','BUSD/USDT','BCH/USDT','ALGO/USDT','MATIC/USDT','XLM/USDT','VET/USDT','ATOM/USDT','ICP/USDT','ICP/USDT','AXS/USDT', 'FTT/USDT','FIL/USDT','FTM/USDT','TRX/USDT','ETC/USDT']

def sendmail(email, coin):
    try:    
        send_mail(
        'Market Finance Notification',
        'The {} you tracked has exceeded the limit. Please visit Market Finance to check'.format(coin),
        'MarketFinanceNT208@gmail.com',
        [email])
    except:
        print("The email invalid")

# def sendnotify():
#     async_to_sync(channel_layer.group_send)('Coin', {'type': 'send_new_data', 'text': data_send})

@shared_task
def send_mail_notify():
    notifys = Notify.objects.filter(isNotify=False)
    for notify in notifys:
        coin = Coin.objects.filter(typeCoin=notify.typeCoin).order_by('-time').first()
        if coin.value > notify.max_threshold or coin.value < notify.min_threshold:
            sendmail(email=notify.owner.email,coin=notify.typeCoin)
            # sendnotify()
            notify.isNotify = True
            notify.save()
