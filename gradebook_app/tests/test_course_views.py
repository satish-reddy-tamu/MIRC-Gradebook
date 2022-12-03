from django.test import TestCase
from django.urls import reverse

from gradebook_app.models.course_model import Course


class TestCourseViews(TestCase):
    def test_display_all_courses(self):
        response = self.client.get(reverse('display_all_courses'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/courses.html")

    def test_add_course_get(self):
        response = self.client.get(reverse('add_course'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/course_form.html")

    def test_add_course_form_invalid(self):
        response = self.client.post(reverse('add_course'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/course_form.html")
        self.assertFalse(response.json()['form_is_valid'])

    def test_add_course_form_valid(self):
        obj = {'course_code': "312", 'name': "student", 'description': "description of course", 'department': "CSCE",
               'year': 2023, 'semester': "Fall", 'credits': "3"}
        response = self.client.post(reverse('add_course'), obj, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.json()['form_is_valid'])

    def test_update_course_get_invalid_id(self):
        response = self.client.get(reverse('update_course', args=[1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

    def test_update_course_get_valid_id(self):
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        response = self.client.get(reverse('update_course', args=[1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/course_form.html")

    def test_update_course_post_invalid_id(self):
        response = self.client.post(reverse('update_course', args=[1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

    def test_update_course_post_valid_id_invalid_form(self):
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        response = self.client.post(reverse('update_course', args=[1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/course_form.html")
        self.assertFalse(response.json()['form_is_valid'])

    def test_update_course_post_valid_id_valid_form(self):
        obj = {'course_code': "312", 'name': "student", 'description': "description of course", 'department': "CSCE",
               'year': 2023, 'semester': "Fall", 'credits': "3"}
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        response = self.client.post(reverse('update_course', args=[1]), obj, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        print(response.json())
        self.assertTrue(response.json()['form_is_valid'])

    def test_delete_course(self):
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        response = self.client.post(reverse('delete_course', args=[10]))
        self.assertEquals(response.status_code, 302)
