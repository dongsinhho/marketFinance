from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("users/login/", views.UserLoginView.as_view()),
    path("users/register/", views.UserRegisterView.as_view(),name='register'),
    path("users/<int:pk>/", views.UserDetail.as_view()),
]  + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)