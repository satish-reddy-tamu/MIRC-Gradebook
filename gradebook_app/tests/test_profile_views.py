from django.test import TestCase
from django.urls import reverse

from gradebook_app.models.profile_model import Profile


class TestProfileViews(TestCase):
    def test_display_all_profiles(self):
        response = self.client.get(reverse('display_all_profiles'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/profiles.html")
    
    def test_add_profile_get(self):
        response = self.client.get(reverse('add_profile'), HTTP_X_REQUESTED_WITH ='XMLHttpRequest' )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/profile_form.html")
    
    def test_add_profile_form_invalid(self):
        response = self.client.post(reverse('add_profile'), HTTP_X_REQUESTED_WITH ='XMLHttpRequest' )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/profile_form.html")
        self.assertFalse(response.json()['form_is_valid'])
    
    def test_add_profile_form_valid(self):
        obj = { 'email': "abc@gmail.com", 'type' : "student", 'first_name' : "John", 'last_name': "Doe", 'department' : "CSCE", 'phone' : "9791234567"}
        response = self.client.post(reverse('add_profile'), obj, HTTP_X_REQUESTED_WITH ='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.json()['form_is_valid'])

    def test_add_bulk_profiles(self):
        response = self.client.get(reverse('add_bulk_profiles'))
        self.assertEquals(response.status_code, 302)

    def test_update_profile_get_invalid_id(self):
        response = self.client.get(reverse('update_profile', args=[1]),HTTP_X_REQUESTED_WITH ='XMLHttpRequest' )
        self.assertEquals(response.status_code, 200)
    

    def test_update_profile_get_valid_id(self):
        Profile.objects.create(email = "abc", type = "pl", first_name = "asd", last_name = "asd", department= "dep", phone = "23123" )
        response = self.client.get(reverse('update_profile', args=[1]),HTTP_X_REQUESTED_WITH ='XMLHttpRequest' )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/profile_form.html")

    def test_update_profile_post_invalid_id(self):
        response = self.client.post(reverse('update_profile', args=[1]),HTTP_X_REQUESTED_WITH ='XMLHttpRequest' )
        self.assertEquals(response.status_code, 200)

    def test_update_profile_post_valid_id_invalid_form(self):
        Profile.objects.create(email = "abc", type = "pl", first_name = "asd", last_name = "asd", department= "dep", phone = "23123" )
        response = self.client.post(reverse('update_profile', args=[1]),HTTP_X_REQUESTED_WITH ='XMLHttpRequest' )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/profile_form.html")
        self.assertFalse(response.json()['form_is_valid'])

    def test_update_profile_post_valid_id_valid_form(self):
        obj = { 'email': "abc@gmail.com", 'type' : "student", 'first_name' : "John", 'last_name': "Doe", 'department' : "CSCE", 'phone' : "9791234567"}
        Profile.objects.create(email = "abc", type = "pl", first_name = "asd", last_name = "asd", department= "dep", phone = "23123" )
        response = self.client.post(reverse('update_profile', args=[1]), obj, HTTP_X_REQUESTED_WITH ='XMLHttpRequest' )
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.json()['form_is_valid'])
    
    def test_delete_profile(self):
        Profile.objects.create(email = "abc", type = "pl", first_name = "asd", last_name = "asd", department= "dep", phone = "23123" )
        response = self.client.post(reverse('delete_profile', args=[10]))
        self.assertEquals(response.status_code, 302)