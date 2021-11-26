from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import *

admin.site.register(Coin)
admin.site.register(Notify)
admin.site.register(TypeCoin)
admin.site.register(FavoriteCoin)
admin.site.register(User, UserAdmin)