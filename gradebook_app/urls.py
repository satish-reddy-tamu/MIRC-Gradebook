from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('get/<str:email>', views.getUser),
    path('add/<str:email>', views.addUser),
    path('getall', views.getAllUsers),
    path('user', views.log_user),

]