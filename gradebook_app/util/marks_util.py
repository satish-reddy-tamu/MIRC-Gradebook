from django.db.models.functions import Round


def calculate_normalized_score(marks, max_marks, weights, total_weight, rnd=True):
    norm_score = 0
    if isinstance(marks, list):
        for mark, max_mark, weight in zip(marks, max_marks, weights):
            norm_score += (mark / max_mark) * (weight / total_weight)
    else:
        norm_score = (marks / max_marks) * (weights / total_weight)
    if rnd:
        return round(norm_score * 100, 2)
    else:
        return Round(norm_score * 100, 2)


def calculate_grade(score, thresholds):
    thresholds = list(map(float, thresholds.split(',')))
    thresholds = [100.0] + thresholds
    grade = ''
    asc = ord('A')
    for i in range(0, len(thresholds) - 1):
        if thresholds[i] >= score > thresholds[i + 1]:
            grade = chr(asc)
            break
        else:
            asc += 1

    return grade if grade else 'F'
