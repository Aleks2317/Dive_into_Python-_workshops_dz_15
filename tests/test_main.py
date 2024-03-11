import pytest

from main import Student


def test_1_enter_name_file():
    student = Student("Иван Иванов", 'subjects.csv')
    assert student.name == "Иван Иванов"


def test_2_enter_name_file():
    student = Student("Иван Иванов", 'subjects.csv')
    assert student.subjects_file == 'subjects.csv'


def test_3_add_grade():
    student = Student("Иван Иванов", 'subjects.csv')
    student.add_grade("Математика", 4)
    assert student.subjects["Математика"]['grades'] == [4]


def test_4_error_name():
    with pytest.raises(ValueError):
        Student("ван Иванов", 'subjects.csv')


def test_5_error_file():
    with pytest.raises(AttributeError):
        Student("Иван Иванов", 'subjects.txt')


def test_6_get_average_test_score():
    with pytest.raises(ValueError):
        student = Student("Иван Иванов", 'subjects.csv')
        student.get_average_test_score("English")


def test_7_get_average_test_score():
    with pytest.raises(ValueError):
        student = Student("Иван Иванов", 'subjects.csv')
        student.get_average_test_score("English")
