from django.contrib.auth.models import User
from django.test import TestCase

from gradebook_app.models.profile_model import Profile


class TestLoginViews(TestCase):
    def test_home_authenticatedUser(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get('/home', {'user': self.user})
        self.assertEquals(response.status_code, 302)

    def test_login_profile_does_not_exist(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        response = self.client.get('/login', {'user': self.user})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "common/profile_not_exists.html")

    def test_login_profile_access_denied(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='abc@gmail.com')
        login = self.client.login(username='testuser', password='12345')
        Profile.objects.create(email="abc@gmail.com", type="pl", first_name="asd", last_name="asd", department="dep",
                               phone="23123")

        response = self.client.get('/login', {'user': self.user})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "common/access_denied.html")

    def test_login_profile_student(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='abc@gmail.com')
        login = self.client.login(username='testuser', password='12345')
        Profile.objects.create(email="abc@gmail.com", type="student", first_name="asd", last_name="asd",
                               department="dep", phone="23123")
        response = self.client.get('/login', {'user': self.user})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "student/home.html")

    def test_login_profile_admin(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='abc@tamu.edu')
        login = self.client.login(username='testuser', password='12345')
        Profile.objects.create(email="abc@tamu.edu", type="admin", first_name="asd", last_name="asd", department="dep",
                               phone="23123")
        response = self.client.get('/login', {'user': self.user})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/home.html")

    def test_login_profile_professor(self):
        self.user = User.objects.create_user(username='testuser', password='12345', email='abc@gmail.com')
        login = self.client.login(username='testuser', password='12345')
        Profile.objects.create(email="abc@gmail.com", type="professor", first_name="asd", last_name="asd",
                               department="dep", phone="23123")
        response = self.client.get('/login', {'user': self.user})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "professor/home.html")
