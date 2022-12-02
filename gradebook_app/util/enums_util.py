from enum import Enum


class Departments(Enum):
    CSCE = "Computer Science and Engineering"
    ECE = "Electronics and Electrical Engineering"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def get_all_departments(cls):
        return [i.name for i in cls]


class ProfileType(Enum):
    STUDENT = "student"
    PROFESSOR = "professor"
    ADMIN = "admin"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.value) for i in cls)

    @classmethod
    def get_all_profiles(cls):
        return [i.value for i in cls]


class Semesters(Enum):
    Fall = "Fall"
    SPRING = "Spring"
    SUMMER = "Summer"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def get_all_semesters(cls):
        return [i.name for i in cls]


class Grades(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def get_all_grades(cls):
        return [i.name for i in cls]


class EvaluationTypes(Enum):
    Assignment = "Assignment"
    Quiz = "Quiz"
    MidExam = "MidExam"
    FinalExam = "FinalExam"
    Miscellaneous = "Miscellaneous"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def get_all_evaluation_types(cls):
        return [i.name for i in cls]