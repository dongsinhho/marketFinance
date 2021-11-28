from .consumer import WSConsummer
from django.urls import path

ws_urlpatterns = [
    path('', WSConsummer.as_asgi())
    # path('notifications/<', NotifyConsummer.as_asgi())
]