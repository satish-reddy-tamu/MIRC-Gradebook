from django.test import TestCase
from django.urls import reverse

from gradebook_app.models.course_model import Course


class TestProfessorViews(TestCase):
    def test_view_course_details(self):
        response = self.client.get(reverse('view_course_details', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "professor/course_details.html")

    def test_view_course_details(self):
        response = self.client.get(reverse('configure_course', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "professor/configure_course.html")

    def test_add_course_configuration(self):
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        evaluations = {"eval1": {'name': "abc", 'eval_type': "type", 'weight': 0.5, 'max_marks': 50.0},
                       "eval2": {'name': "abc2", 'eval_type': "type2", 'weight': 0.5, 'max_marks': 50.0}}
        session = self.client.session
        session['evaluations'] = evaluations
        session['grade_function'] = "60"
        session.save()
        response = self.client.get(reverse('add_course_configuration', args=[1]))
        self.assertEquals(response.status_code, 302)

    def test_view_students_list(self):
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        response = self.client.get(reverse('view_students_list', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "professor/students_list.html")

    def test_evaluations_list(self):
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        response = self.client.get(reverse('evaluations_list', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "professor/evaluations_list.html")

    def test_get_add_evaluation(self):
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        response = self.client.get(reverse('add_evaluation', args=[1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "professor/evaluation_form.html")

    def test_post_add_evaluation_invalid_form(self):
        evaluations = {"eval1": {'name': "abc", 'eval_type': "type", 'weight': 0.5, 'max_marks': 50.0},
                       "eval2": {'name': "abc2", 'eval_type': "type2", 'weight': 0.5, 'max_marks': 50.0}}
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        session = self.client.session
        session['evaluations'] = evaluations
        session['eval_id'] = "1"
        session.save()
        response = self.client.post(reverse('add_evaluation', args=[1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.json()['form_is_valid'])

    def test_post_add_evaluation_valid_form(self):
        evaluations = {"eval1": {'name': "abc", 'eval_type': "type", 'weight': 0.5, 'max_marks': 50.0},
                       "eval2": {'name': "abc2", 'eval_type': "type2", 'weight': 0.5, 'max_marks': 50.0}}
        obj = {'name': "abc", 'eval_type': "Quiz", 'weight': 0.5, 'max_marks': 50.0}
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        session = self.client.session
        session['evaluations'] = evaluations
        session['eval_id'] = "1"
        session.save()
        response = self.client.post(reverse('add_evaluation', args=[1]), obj, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.json()['form_is_valid'])

    def test_get_update_evaluation_exception(self):
        evaluations = {"eval1": {'name': "abc", 'eval_type': "type", 'weight': 0.5, 'max_marks': 50.0},
                       "eval2": {'name': "abc2", 'eval_type': "type2", 'weight': 0.5, 'max_marks': 50.0}}
        session = self.client.session
        session['evaluations'] = evaluations
        session['eval_id'] = "1"
        session.save()
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        response = self.client.get(reverse('update_evaluation', args=[1, 1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)

    def test_get_update_evaluation(self):
        evaluations = {"1": {'name': "abc", 'eval_type': "type", 'weight': 0.5, 'max_marks': 50.0},
                       "eval2": {'name': "abc2", 'eval_type': "type2", 'weight': 0.5, 'max_marks': 50.0}}
        session = self.client.session
        session['evaluations'] = evaluations
        session['eval_id'] = "1"
        session.save()
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        response = self.client.get(reverse('update_evaluation', args=[1, 1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "professor/evaluation_form.html")

    def test_post_update_evaluation_valid_form(self):
        evaluations = {"1": {'name': "abc", 'eval_type': "type", 'weight': 0.5, 'max_marks': 50.0},
                       "eval2": {'name': "abc2", 'eval_type': "type2", 'weight': 0.5, 'max_marks': 50.0}}
        obj = {'name': "abc", 'eval_type': "FinalExam", 'weight': 0.5, 'max_marks': 50.0}
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits=3)
        session = self.client.session
        session['evaluations'] = evaluations
        session['eval_id'] = "1"
        session.save()
        response = self.client.post(reverse('update_evaluation', args=[1, 1]), obj,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.json()['form_is_valid'])

    def test_post_update_evaluation_invalid_form(self):
        evaluations = {"1": {'name': "abc", 'eval_type': "type", 'weight': 0.5, 'max_marks': 50.0},
                       "eval2": {'name': "abc2", 'eval_type': "type2", 'weight': 0.5, 'max_marks': 50.0}}
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits=3)
        session = self.client.session
        session['evaluations'] = evaluations
        session['eval_id'] = "1"
        session.save()
        response = self.client.post(reverse('update_evaluation', args=[1, 1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.json()['form_is_valid'])

    def test_delete_evaluation(self):
        evaluations = {"1": {'name': "abc", 'eval_type': "type", 'weight': 0.5, 'max_marks': 50.0},
                       "eval2": {'name': "abc2", 'eval_type': "type2", 'weight': 0.5, 'max_marks': 50.0}}
        session = self.client.session
        session['evaluations'] = evaluations
        session['eval_id'] = "1"
        session.save()
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        response = self.client.get(reverse('delete_evaluation', args=[1, 1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 302)

    def test_delete_evaluation_exception(self):
        evaluations = {"eval1": {'name': "abc", 'eval_type': "type", 'weight': 0.5, 'max_marks': 50.0},
                       "eval2": {'name': "abc2", 'eval_type': "type2", 'weight': 0.5, 'max_marks': 50.0}}
        session = self.client.session
        session['evaluations'] = evaluations
        session['eval_id'] = "1"
        session.save()
        Course.objects.create(course_code="313", name="student", description="description", department="CSCE",
                              year=2023, semester="Fall", credits="3")
        response = self.client.get(reverse('delete_evaluation', args=[1, 1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 302)

    def test_get_add_grade_function(self):
        response = self.client.get(reverse('add_grade_function', args=[1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "professor/evaluation_form.html")

    def test_post_add_grade_function_invalid_form(self):
        response = self.client.post(reverse('add_grade_function', args=[1]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "professor/evaluation_form.html")
        self.assertFalse(response.json()['form_is_valid'])

    def test_post_add_grade_function_valid_form(self):
        obj = {'A': 90, 'B': 80, 'C': 70, 'D': 60, 'E': 50, 'F': 40}
        response = self.client.post(reverse('add_grade_function', args=[1]), obj,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.json()['form_is_valid'])
