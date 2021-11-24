from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
    
class TypeCoin(models.Model):
    name = models.CharField(max_length=100)
    imageURL = models.URLField(max_length=255)
    ranked = models.IntegerField()


#Cần lưu ý type coin của user
class User(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=255)
    typeCoin = models.ForeignKey(TypeCoin, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_created=True,auto_now=True)
    #notify = 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    def __str__(self):
        return self.username


class Coin(models.Model):
    time = models.DateTimeField(auto_now=True, auto_created=True)
    value = models.FloatField(default=0, blank=True)
    typeCoin = models.ForeignKey(TypeCoin, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.typeCoin)


class Notify(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    typeCoin = models.ForeignKey(Coin,on_delete=models.CASCADE)
    max_threshold = models.DecimalField(decimal_places=20, max_digits=50)
    min_threshold = models.DecimalField(decimal_places=20, max_digits=50)
    isNotify = models.BooleanField(default=False)
    created = models.DateTimeField(auto_created=True,auto_now=True)
