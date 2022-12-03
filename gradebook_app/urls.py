from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

from gradebook_app.views.admin import course_view
from gradebook_app.views.admin import profile_view
from gradebook_app.views.common import login_view
from gradebook_app.views.professor import dashboard_view
from gradebook_app.views.student import student_dashboard_view

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
    path('admin/courses/enroll/<int:id>', course_view.enroll, name='enroll'),

    # professor
    path('professor/course/<int:id>', dashboard_view.view_course_details, name='view_course_details'),
    path('professor/course/<int:id>/configure', dashboard_view.configure_course, name='configure_course'),
    path('professor/course/<int:id>/configure/submit', dashboard_view.add_course_configuration,
         name='add_course_configuration'),
    path('professor/course/<int:id>/students', dashboard_view.view_students_list, name='view_students_list'),
    path('professor/course/<int:course_id>/students/<int:profile_id>/update', dashboard_view.update_student_evaluation, name='update_student_evaluation'),
    path('professor/course/<int:id>/evaluations', dashboard_view.evaluations_list, name='evaluations_list'),
    path('professor/course/<int:id>/evaluations/add', dashboard_view.add_evaluation, name='add_evaluation'),
    path('professor/course/<int:id>/evaluations/add_bulk', dashboard_view.add_bulk_evaluations, name='add_bulk_evaluations'),
    path('professor/course/<int:course_id>/evaluations/update/<int:eval_id>', dashboard_view.update_evaluation,
         name='update_evaluation'),
    path('professor/course/<int:course_id>/evaluations/delete/<int:eval_id>', dashboard_view.delete_evaluation,
         name='delete_evaluation'),
    path('professor/course/<int:id>/evaluations/add_grade_function', dashboard_view.add_grade_function,
         name='add_grade_function'),

    # student
    path('student/<int:profile_id>/course/<int:course_id>', student_dashboard_view.view_course_details, name='student_view_course_details'),


]
