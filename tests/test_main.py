import pytest
from contextlib import nullcontext as does_not_raise
from main import Student


class TestStudent:
    @pytest.mark.parametrize(
        "name, file, res, expectation",
        [
            ("Иван Иванов", 'subjects.csv', "Иван Иванов", does_not_raise()),
            ("иван Иванов", 'subjects.csv', "иван Иванов", pytest.raises(ValueError)),
            ("Иван иванов", 'subjects.csv', "Иван иванов", pytest.raises(ValueError)),
            ("Иванов", 'subjects.csv', "Иванов", pytest.raises(ValueError)),
            ("", 'subjects.csv', "", pytest.raises(ValueError)),
        ]
    )
    def test_1_enter_name_file(self, name, file, res, expectation):
        with expectation:
            student = Student(name, file)
            assert student.name == res

    @pytest.mark.parametrize(
        "name, file, res, expectation",
        [
            ("Иван Иванов", 'subjects.csv', 'subjects.csv', does_not_raise()),
            ("Иван Иванов", 'subjects.cs', 'subjects.cs', pytest.raises(AttributeError)),
            ("Иван Иванов", '', "", pytest.raises(AttributeError)),
            ("Иван Иванов", 'subjects.txt', 'subjects.txt', pytest.raises(AttributeError)),
            ("Иван Иванов", 'subjects.doc', "subjects.doc", pytest.raises(AttributeError)),
        ]
    )
    def test_2_enter_name_file(self, name, file, res, expectation):
        with expectation:
            student = Student(name, file)
            assert student.subjects_file == res

    @pytest.mark.parametrize(
        "name, file, subject, grade, res, expectation",
        [
            ("Иван Иванов", 'subjects.csv', 'Математика', 4, [4], does_not_raise()),
            ("Иван Иванов", 'subjects.csv', 'Физика', 5, [5], does_not_raise()),
            ("Иван Иванов", 'subjects.csv', 'История', 5, [5], does_not_raise()),
            ("Иван Иванов", 'subjects.csv', 'Литература', -5, [-5], pytest.raises(ValueError)),
            ("Иван Иванов", 'subjects.csv', 'Литература', 5.2, [5.2], pytest.raises(ValueError)),
        ]
    )
    def test_3_add_grade(self, name, file, subject, grade, res, expectation):
        with expectation:
            student = Student(name, file)
            student.add_grade(subject, grade)
            assert student.subjects[subject]['grades'] == res

    def test_4_error_name(self):
        with pytest.raises(ValueError):
            Student("ван Иванов", 'subjects.csv')

    def test_5_error_file(self):
        with pytest.raises(AttributeError):
            Student("Иван Иванов", 'subjects.txt')

    def test_6_get_average_test_score(self):
        with pytest.raises(ValueError):
            student = Student("Иван Иванов", 'subjects.csv')
            student.get_average_test_score("English")

    def test_7_get_average_test_score(self):
        with pytest.raises(ValueError):
            student = Student("Иван Иванов", 'subjects.csv')
            student.get_average_test_score("English")

