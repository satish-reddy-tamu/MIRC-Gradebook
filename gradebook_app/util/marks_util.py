def calculate_normalized_score(score, min_score, max_score):
    return (score - min_score) / (max_score - min_score) * 100





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
