from src.class_save_csv import Saver

class Mylist:
    """
    Этот класс для работы со списком вакансий.
    """
    def __init__(self):
        self.vacancy_list = []
        self.csv_saver = Saver()

    def __len__(self):
        return len(self.vacancy_list)

    def clear_list(self):
        """
        Удалить все вакансии из списка
        """
        self.vacancy_list.clear()

    def add_vacancy(self, vacancy: object):
        """
        Добавление вакансии в список
        """
        self.vacancy_list.append(vacancy)

    def get_vacancy(self, index: int):
        """
        Получение вакансии по индексу
        """
        return self.vacancy_list[index-1]

    def delete_vacancy(self, vacancy: object):
        """
        Удаление одной вакансии из списка
        """
        if vacancy in self.vacancy_list:
            self.vacancy_list.remove(vacancy)
        else:
            pass

    def sorting_vacancies_data(self):
        """
        Сортировка вакансий в списке по дате
        """
        self.vacancy_list.sort(reverse=True, key=lambda vacancy: vacancy.data_published)

    def sorting_vacancies_salary(self):
        """
        Сортировка вакансий в списке по средней зарплате
        """
        self.vacancy_list.sort(reverse=True, key=lambda vacancy: vacancy.salary_average)

    def filter_list_word(self, word: str):
        """
        Фильтровать вакансии по слову пользователя
        """
        delete_list = []
        for vacancy in self.vacancy_list:
            if word in vacancy.requirement or word in vacancy.name:
                pass
            else:
                delete_list.append(vacancy)
        for vacancy in delete_list:
            self.vacancy_list.remove(vacancy)
        return self

    def filter_list_salary(self, salary: int):
        """
        Фильтровать вакансии по зарплате от пользователя
        """
        delete_list = []
        for vacancy in self.vacancy_list:
            if vacancy.salary_average >= salary:
                pass
            else:
                delete_list.append(vacancy)
        for vacancy in delete_list:
            self.vacancy_list.remove(vacancy)
        return self

    def save_csv(self):
        """
        Сохранение вакансий в списке в CSV-файле
        """
        path = self.csv_saver.save_vacancies_csv(self.vacancy_list)
        return path

    def save_xlsx(self):
        pass

    def __str__(self):
        return '\n'.join([f'Vacancy N {index+1}\n{vacancy.__str__()}' for index, vacancy in enumerate(self.vacancy_list)])