from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='home')),
    path('home', views.home),
    path('login', views.login),
    path('contact', TemplateView.as_view(template_name="contact.html")),
    path('accounts/', include('allauth.urls'))
]
