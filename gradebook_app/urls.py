from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('login', views.login),
    path('accounts/', include('allauth.urls'))
]
