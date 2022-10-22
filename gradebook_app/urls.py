from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

from gradebook_app.models.profile_model import ProfileForm
from gradebook_app.views.common import login_view
from gradebook_app.views.admin import profile_view
from gradebook_app.views.admin import course_view

urlpatterns = [
    path('', RedirectView.as_view(url='home')),
    path('home', login_view.home),
    path('login', login_view.login),
    path('contact', TemplateView.as_view(template_name="common/contact.html")),
    path('accounts/', include('allauth.urls')),

    # admin
    path('admin/profiles', profile_view.display_all_profiles, name='display_all_profiles'),
    path('admin/profiles/add_bulk', profile_view.add_bulk_profiles, name='add_bulk_profiles'),
    path('admin/profiles/add', profile_view.add_profile, name='add_profile'),
    path('admin/profiles/update/<int:id>', profile_view.update_profile, name='update_profile'),
    path('admin/profiles/delete/<int:id>', profile_view.delete_profile, name='delete_profile'),
    path('admin/courses', course_view.display_all_courses, name='display_all_courses'),
    path('admin/courses/add', course_view.add_course, name='add_course'),
    path('admin/courses/update/<int:id>', course_view.update_course, name='update_course'),
    path('admin/courses/delete/<int:id>', course_view.delete_course, name='delete_course'),
]
