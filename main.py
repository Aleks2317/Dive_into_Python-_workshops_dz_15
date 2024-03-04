import csv


class Val:
    def __init__(self, name: str = None, subjects_file = None):
        self.name = name
        self.subjects_file = subjects_file

    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.name, value)

    def validate(self, value, ):
        print(value, value.split()[0].isalpha(), value[0].isupper())  # # # !
        if self.name is None and (not value.split()[0].isalpha() or not value[0].isupper()):
            raise ValueError(f'ФИО должно состоять только из букв и начинаться с заглавной буквы')
        print(value[-4:])
        if self.name is not None and value[-4:] != self.name:
            raise ValueError('Предмет {Название предмета} не найден')


class Student:
    name = Val()

    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects = {}
        self.load_subjects(subjects_file)

    def load_subjects(self, subjects_file):
        with open(subjects_file, 'w', newline='') as f:
            subjects = csv.reader(f)
            for subject in subjects:
                if subject not in self.subjects:  # ?
                    self.subjects[subject] = {'grades': [], 'test_scores': []}

    def add_grade(self, subject, grade):
        self.subjects[subject]['grade'].append(grade)

    def add_test_score(self, subject, test_score):
        self.subjects[subject]['test_score'].append(test_score)

    def get_average_test_score(self, subject):
        aver_test = self.subjects[subject]['test_score']
        return sum(aver_test) / len(aver_test)

    def get_average_grade(self):
        average_grade = 0
        count = 0
        for subj in self.subjects:
            average_grade += sum(subj['grade'])
            count += len(subj['grade'])
        return average_grade / count

    def __str__(self):
        # if list(self.subjects.keys()) != []:
        #     subjec = ','.join(self.subjects.keys())
        return f"Студент: {self.name}\nПредметы: {self.subjects}"


if __name__ == '__main__':
    student = Student("Иван Иванов", "subjects.csv")

    # student.add_grade("Математика", 4)
    # student.add_test_score("Математика", 85)
    #
    # student.add_grade("История", 5)
    # student.add_test_score("История", 92)
    #
    # average_grade = student.get_average_grade()
    # print(f"Средний балл: {average_grade}")
    #
    # average_test_score = student.get_average_test_score("Математика")
    # print(f"Средний результат по тестам по математике: {average_test_score}")
    #
    # print(student)
