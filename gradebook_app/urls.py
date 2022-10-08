from django.urls import path, include
from . import views

urlpatterns = [
    path('/', views.home),
    path('login', views.login),
    path('accounts/', include('allauth.urls')),
]
