from django.shortcuts import redirect
from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', lambda request: redirect('home/', permanent=False)),
    path('accounts/', include('allauth.urls')),
    path('home/', views.home),
    path('login/', views.login),
]
