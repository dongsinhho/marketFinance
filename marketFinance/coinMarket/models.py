from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=255)
    created = models.DateTimeField(auto_created=True,auto_now=True)

class Coin(models.Model):
    time = models.DateTimeField(auto_now=True, auto_created=True)
    typeCoin = models.CharField(max_length=100)
    value = models.FloatField(default=0, blank=True)
    def __str__(self):
        return str(self.typeCoin)

# class CoinManager(models.Manager):
#     def create_coin(self, typeCoin, value):
#         coin = self.create(typeCoin=typeCoin, value=value)
#         # do something with the book
#         return coin
    

class Notify(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    typeCoin = models.ForeignKey(Coin,on_delete=models.CASCADE)
    max_threshold = models.DecimalField(decimal_places=20, max_digits=50)
    min_threshold = models.DecimalField(decimal_places=20, max_digits=50)
    isNotify = models.BooleanField(default=False)
    created = models.DateTimeField(auto_created=True,auto_now=True)
