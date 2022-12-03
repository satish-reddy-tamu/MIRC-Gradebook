from django import forms

from gradebook_app.models import Marks, Evaluation, Course, ProfileCourse, Profile
from gradebook_app.util.marks_util import calculate_normalized_score, calculate_grade


class EvaluationsUploadForm(forms.Form):
    Evaluation_Marks = forms.FileField()

    def __init__(self, evaluations, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["Evaluation_Name"] = forms.ChoiceField(choices=evaluations)

    def save(self, course_id, data, file):

        current_eval_id = data['Evaluation_Name']
        total_eval_objs = Evaluation.objects.filter(course_id=course_id).all()
        file_data = file['Evaluation_Marks'].read().decode('utf-8').split('\n')
        course = Course.objects.filter(id=course_id).all()
        for item in file_data[1:]:
            if not item.strip():
                continue
            email, marks = item.split(',')
            marks = float(marks)
            profile_id = Profile.objects.filter(email=email).all()[0].id
            update_success = Marks.objects.filter(profile_id=profile_id,
                                                  course_id=course_id,
                                                  evaluation_id=current_eval_id
                                                  ).update(marks=marks)
            if not update_success:
                Marks(profile_id=profile_id, course_id=course_id, evaluation_id=current_eval_id, marks=marks).save()

            weights_list = []
            marks_list = []
            max_marks_list = []
            for eval in total_eval_objs:
                current_eval_marks = Marks.objects.filter(profile_id=profile_id,
                                                          course_id=course_id,
                                                          evaluation_id=eval.id).values('marks')
                if current_eval_marks:
                    weights_list.append(eval.weight)
                    marks_list.append(current_eval_marks[0]['marks'])
                    max_marks_list.append(eval.max_marks)

            thresholds = course[0].thresholds
            score = calculate_normalized_score(marks_list, max_marks_list, weights_list, sum(weights_list))
            grade = calculate_grade(score, thresholds)
            ProfileCourse.objects.filter(profile_id=profile_id, course_id=course_id).update(
                score=score,
                grade=grade
            )
