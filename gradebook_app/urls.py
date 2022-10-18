from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

from .views.common import login_view
from gradebook_app.views.admin import profile_view

urlpatterns = [
    path('', RedirectView.as_view(url='home')),
    path('home', login_view.home),
    path('login', login_view.login),
    path('contact', TemplateView.as_view(template_name="common/contact.html")),
    path('accounts/', include('allauth.urls')),

    # admin
    path('admin/profiles', TemplateView.as_view(template_name="admin/profiles.html")),
    path('admin/profiles/add_bulk', profile_view.add_bulk_profiles, name='add_bulk_profiles')

]
