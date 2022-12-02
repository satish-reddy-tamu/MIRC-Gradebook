from django import forms

from gradebook_app.models import Marks, Evaluation, ProfileCourse, Course
from gradebook_app.util.marks_util import calculate_normalized_score, calculate_grade


class EvaluationEditForm(forms.Form):

    def __init__(self, instance):
        super().__init__()
        for eval_id, eval_name, marks, max_marks in instance:
            eval = f"{eval_name} ({eval_id})"
            self.fields[eval] = forms.FloatField(min_value=0, max_value=max_marks, required=False)
            self.initial[eval] = marks

    def save(self, course_id, profile_id, data):
        weighted_score = 0
        max_score = 0
        for evaluation, marks in data.items():
            if evaluation != "csrfmiddlewaretoken":
                eval_id = int(evaluation.split('(')[1].split(')')[0])
                if marks.strip():
                    marks = float(marks)
                    update_success = Marks.objects.filter(profile_id=profile_id, course_id=course_id, evaluation_id=eval_id).update(
                        marks=marks)
                    if not update_success:
                        Marks(profile_id=profile_id, course_id=course_id, evaluation_id=eval_id, marks=marks).save()
                    eval_obj = Evaluation.objects.filter(id=eval_id).all()
                    weighted_score += eval_obj[0].weight * marks
                    max_score += eval_obj[0].weight * eval_obj[0].max_marks
        course = Course.objects.filter(id=course_id).all()
        thresholds = course[0].thresholds
        score = calculate_normalized_score(weighted_score, 0, max_score)
        grade = calculate_grade(score, thresholds)
        ProfileCourse.objects.filter(profile_id=profile_id, course_id=course_id).update(
            score=score,
            grade=grade
        )
