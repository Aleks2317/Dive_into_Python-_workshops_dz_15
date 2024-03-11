import argparse
import csv
import logging


FORMAT = '{levelname:<8} :: {asctime}.\n В "{name}" в строке {lineno:03d} ' \
         'функция "{funcName}()" записано ::\n:: {msg}\n'
logging.basicConfig(
    filename=f'logs_.log',
    encoding='utf-8',
    level=logging.ERROR,
    format=FORMAT,
    style='{',
    filemode='w',
)


logger = logging.getLogger(__name__)


class Descriptor:

    def __init__(self, extension: str = None):
        self.extension = extension
        self.logger = logging.getLogger(__name__)

    def __set_name__(self, owner, name):
        """Дандер занимается инкапсуляцией"""
        self.logger.debug(f'__set_name__: {self = }, {owner = }, {name = }')
        self.param_name = '_' + name

    def __get__(self, instance, name):
        """ Функция для получения у объекта instance (значения для свойства self.param_name)"""
        self.logger.debug(f'__get__: {self = }, {instance = }, {name = }')
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        """ Проверяет установку атрибута."""
        if self.__dict__['param_name'] == '_name':
            self.valid_name(value)
        if self.__dict__['param_name'] == '_subjects_file':
            self.valid_subject(value)
        self.logger.debug(f'__set__: {self = }, {instance = }, {value = }')
        setattr(instance, self.param_name, value)

    def valid_name(self, name: str):
        """ Проверяет ФИО на первые заглавные буквы"""
        self.logger.debug(f'valid_name(: {self = }, {name = }')
        name, surname = name.split()
        if name[0].islower() or surname[0].islower():
            self.logger.error("ФИО должно состоять только из букв и начинаться с заглавной буквы")
            raise ValueError("ФИО должно состоять только из букв и начинаться с заглавной буквы")

    def valid_subject(self, subject_file: str):
        """ Проверяет расширение загружаемого файла предметов """
        self.logger.debug(f'valid_name(: {self = }, {subject_file = }')
        if subject_file[-4:] != self.extension:
            self.logger.error("Загружаемый файл должен быть с расширением .csv!")
            raise AttributeError('Загружаемый файл должен быть с расширением .csv!')


class Student:
    """ Класс Student, представляет студента и его успехи по предметам.
    Методы и атрибуты:

    # load_subjects(self, subjects_file): Загружает предметы из файла CSV.
    Использует модуль csv для чтения данных из файла и добавляет предметы в атрибут subjects

    # add_grade(self, subject, grade): Добавляет оценку по заданному предмету.
    Убеждается, что оценка является целым числом от 2 до 5.

    # add_test_score(self, subject, test_score): Добавляет результат теста по заданному предмету.
    Убеждается, что результат теста является целым числом от 0 до 100.

    # get_average_test_score(self, subject): Возвращает средний балл по тестам для заданного предмета.

    # get_average_grade(self): Возвращает средний балл по всем предметам.

    # При помощи класса Descriptor - проверяет при создании класса
    атрибут "name" на первую заглавную букву и наличие только букв,
    и атрибут "subjects_file" на принадлежность файла формату CSV.
    """
    name = Descriptor()
    subjects_file = Descriptor(extension='.csv')

    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects = {}
        self.subjects_file = subjects_file
        self.load_subjects(self.subjects_file)
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f'Start work class Student. You enter:{name = } - {subjects_file = } ')

    def load_subjects(self, subjects_file):
        """ Загружает предметы из файла CSV.
        Использует модуль csv для чтения данных из файла и добавляет предметы в атрибут subjects
        """
        with open(subjects_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                subject = row[0]
                if subject not in self.subjects:
                    self.subjects[subject] = {'grades': [], 'test_scores': []}

    def add_grade(self, subject, grade):
        """ Добавляет оценку по заданному предмету. Убеждается, что оценка является целым числом от 2 до 5. """
        if subject not in self.subjects:
            self.subjects[subject] = {'grades': [], 'test_scores': []}
        if not isinstance(grade, int) or grade < 2 or grade > 5:
            self.logger.error("Оценка должна быть целым числом от 2 до 5")
            raise ValueError("Оценка должна быть целым числом от 2 до 5")
        self.subjects[subject]['grades'].append(grade)

    def add_test_score(self, subject, test_score):
        """  Добавляет результат теста по заданному предмету. Убеждается, что результат теста является целым числом
        от 0 до 100. """
        if subject not in self.subjects:
            self.subjects[subject] = {'grades': [], 'test_scores': []}
        if not isinstance(test_score, int) or test_score < 0 or test_score > 100:
            self.logger.error("Результат теста должен быть целым числом от 0 до 100")
            raise ValueError("Результат теста должен быть целым числом от 0 до 100")
        self.subjects[subject]['test_scores'].append(test_score)

    def get_average_test_score(self, subject):
        """  Возвращает средний балл по тестам для заданного предмета. """
        if subject not in self.subjects:
            raise ValueError(f"Предмет {subject} не найден")
        test_scores = self.subjects[subject]['test_scores']
        if len(test_scores) == 0:
            return 0
        return sum(test_scores) / len(test_scores)

    def get_average_grade(self):
        """ Возвращает средний балл по всем предметам. """
        total_grades = []
        for subject in self.subjects:
            grades = self.subjects[subject]['grades']
            if len(grades) > 0:
                total_grades.extend(grades)
        if len(total_grades) == 0:
            return 0
        return sum(total_grades) / len(total_grades)

    def __str__(self):
        return f"Студент: {self.name}\nПредметы: {', '.join(self.subjects.keys())}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='class Student',
                                     description='Student class, represents the student and his progress in subjects. '
                                                 'Required argument for launching from the console line student name.',
                                     )
    parser.add_argument('file',
                        metavar='name_subjects_file.csv',
                        type=str,
                        help='Enter class Student with argument = name_subjects_file.csv',
                        )

    args = parser.parse_args()
    file = args.file
    student = Student("Иван Иванов", file)
    student.add_grade("Математика", 4)
    student.add_test_score("Математика", 85)

    student.add_grade("История", 5)
    student.add_test_score("История", 92)

    average_grade = student.get_average_grade()
    print(f"Средний балл: {average_grade}")

    average_test_score = student.get_average_test_score("Математика")
    print(f"Средний результат по тестам по математике: {average_test_score}")

    print(student)


