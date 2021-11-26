from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=255)
    avatar = models.ImageField(default=None, upload_to='images')
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    create = models.DateTimeField(auto_created=True, auto_now=True)
    favoriteCoin = models.Aggregate
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    def __str__(self):
        return self.username

class TypeCoin(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(default=None, upload_to='images')
    ranked = models.IntegerField(default=None)
    def __str__(self):
        return self.name

class Coin(models.Model):
    time = models.DateTimeField(auto_now=True, auto_created=True)
    typeCoin = models.ForeignKey(TypeCoin, on_delete=models.CASCADE)
    value = models.FloatField(default=0, blank=True)
    def __str__(self):
        return str(self.time, "    ", self.typeCoin)
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
