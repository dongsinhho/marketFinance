from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("users/login", views.UserLoginView.as_view()),
    path("users/register", views.UserRegisterView.as_view(),name='register'),
    path("users/detail", views.UserDetail.as_view()),
    path("coins/info", views.CoinInfo.as_view()),
    path("coins/<str:time>/<int:pk>", views.CoinData.as_view()),
    path("users/notification", views.CreateNotification.as_view()),
    path("users/notification/<int:pk>", views.DeleteUpdateNotification.as_view()),
    path("users/favorite", views.FavoriteCoinView.as_view())
]  + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)