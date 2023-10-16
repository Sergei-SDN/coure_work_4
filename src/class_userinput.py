from src.classes_api import HeadHunterAPI, SuperJobAPI
from src.class_mylist import Mylist
from src.class_vacancy import Vacancy
import copy

class Userinput:
    """
    Этот класс предназначен для взаимодействия с пользователем в консоли.
    """
    new_param = {
            'website': [],
            'city': [],
            'words': [],
            'date': 14
        }

    def __init__(self):
        self.hh_api = HeadHunterAPI()
        self.sj_api = SuperJobAPI()
        self.all_list = Mylist()
        self.mylist = Mylist()
        self.param = copy.deepcopy(self.new_param)

    def __call__(self):
        """
        Первое меню пользователя.
        """
        while True:
            print('Команды:')
            print('1 - Поиск вакансии')

            if self.mylist.vacancy_list != []:
                print('2 - Показать понравившиеся вакансии')

            print('0 - Выход')
            user_input = input()

            if user_input == '0':
                quit()
            elif user_input == '1':
                self.choosing_parameters()
            elif user_input == '2':
                print(self.mylist)
            else:
                print('Неизвестная команда')

    def choosing_parameters(self):
        """
        Второе меню выбора параметров поиска
        """
        while True:
            self.delete_duplicates()
            print('Вам нужно выбрать сайты, город, дату и слова для поиска')
            print(f'Мы ищем вакансии за последние {self.param["date"]} дней')
            if self.param['website'] != []:
                print(f"Вы выбрали следующий сайт - {', '.join(self.param['website'])}")
            if self.param['city'] != []:
                print(f"Вы выбрали следующий город - {', '.join(self.param['city'])}")
            if self.param['words'] != []:
                print(f"Вы выбрали следующие слова - {', '.join(self.param['words'])}")
            print('1 - выбрать веб-сайты')
            print('2 - добавить слова для поиска')
            print('3 - выбрать город')
            print('4 - изменить дату поиска (по умолчанию последние 14 дней)')
            if self.param['website'] != [] and self.param['city'] != [] and self.param['words'] != []:
                print('5 - поиск вакансий')
            print('0 - Выход')
            user_input = input()

            if user_input == '0':
                self.__call__()
            elif user_input == '1':
                self.choosing_website()
            elif user_input == '2':
                self.choosing_words()
            elif user_input == '3':
                self.choosing_city()
            elif user_input == '4':
                self.choosing_date()
            elif user_input == '5':
                self.research_vacancies()
            else:
                print('Неизвестная команда')

    def choosing_website(self):
        """
        Меню выбора сайтов
        """
        while True:
            print('Мы можем искать вакансии в HeadHunter и SuperJob. Какой сайт вы хотели бы выбрать?')
            print('1 - HeadHunter')
            print('2 - SuperJob')
            print('3 - HeadHunter and SuperJob')
            print('0 - Выход')
            user_input = input()

            if user_input == '0':
                break
            elif user_input == '1':
                self.param['website'].append('HeadHunter')
                break
            elif user_input == '2':
                self.param['website'].append('SuperJob')
                break
            elif user_input == '3':
                self.param['website'].append('HeadHunter')
                self.param['website'].append('SuperJob')
                break
            else:
                print('Неизвестная команда')

    def choosing_words(self):
        """
        Меню для добавления и удаления слов для поиска
        """
        while True:
            self.delete_duplicates()
            if self.param['words'] != []:
                print(f"Вы выбрали следующие слова - {', '.join(self.param['words'])}")
            print('Добавьте слово для поиска или введите «delete», чтобы удалить все слова, или нажмите 0 для выхода.')
            user_input = input().lower()
            if user_input == '0':
                break
            elif user_input == 'delete':
                self.param['words'].clear()
                break
            else:
                self.param['words'].append(user_input)
                break

    def choosing_city(self):
        """
        Добавление города для поиска
        """
        print('Добавьте город для поиска или нажмите 0 для выхода.')
        while True:
            user_input = input().lower()
            if user_input == '0':
                break
            if self.check_city(user_input):
                self.param['city'].append(user_input)
                break
            else:
                print('Попробуйте еще раз. Потому что мы не нашли этот город или нажмите 0 для выхода.')

    def check_city(self, user_input:str):
        """
        Проверка города от пользователя
        """
        if self.hh_api.saver_areas.open_and_find_info(user_input) or self.sj_api.saver_areas.open_and_find_info(user_input):
            return True
        else:
            return False

    def choosing_date(self):
        """
        Выбор количества дней для поиска
        :return:
        """
        while True:
            print('Выберите количество дней для поиска')
            print('1 - 1 день')
            print('2 - 7 дней')
            print('3 - 14 дней')
            print('4 - 30 дней')
            print('0 - Выход')
            user_input = input()
            if user_input == '0':
                break
            elif user_input == '1':
                self.param['date'] = 1
                break
            elif user_input == '2':
                self.param['date'] = 7
                break
            elif user_input == '3':
                self.param['date'] = 14
                break
            elif user_input == '4':
                self.param['date'] = 30
                break
            else:
                print('Неизвестная команда')

    def research_vacancies(self):
        """
        Получение вакансий от HH и SJ, создание объектов класса Vacancy.
        """
        if 'HeadHunter' in self.param['website']:
            if self.param['city'] != []:
                for item in range(len(self.param['city'])):
                    self.hh_api.add_area(self.param['city'][item])
            if self.param['words'] != []:
                self.hh_api.add_words(self.param['words'])
            self.hh_api.change_date(self.param['date'])

            vacancies_hh = self.hh_api.get_vacancies()

            if vacancies_hh != []:
                for item in vacancies_hh:
                   vacancy = Vacancy.create_vacancy_from_hh(item)
                   self.all_list.add_vacancy(vacancy)

        if 'SuperJob' in self.param['website']:
            if self.param['city'] != []:
                for item in range(len(self.param['city'])):
                    self.sj_api.add_area(self.param['city'][item])
            if self.param['words'] != []:
                self.sj_api.add_words(self.param['words'])
            self.sj_api.change_date(self.param['date'])

            vacancies_sj = self.sj_api.get_vacancies()

            if vacancies_sj != []:
                for item in vacancies_sj:
                   vacancy = Vacancy.create_vacancy_from_sj(item)
                   self.all_list.add_vacancy(vacancy)

        self.param = copy.deepcopy(self.new_param)

        self.sorting_vacancies()

    def sorting_vacancies(self):
        """
        Меню сортировки и фильтрации вакансий
        """
        while True:
            print(f'Мы нашли : {len(self.all_list)} вакансий. Мы можем сортировать или фильтровать их. Что нам делать?')
            print('1 - сортировка вакансий по дате')
            print('2 - сортировка вакансий по зарплате')
            print('3 - вывести вакансий по встречающимся словам')
            print('4 - вывести вакансий по веденной зарплате')
            print('5 - Показать все вакансии')
            print('6 - сохранить все вакансии в CSV-файле')
            print('7 - сохранить все вакансии в XLSX-file')
            print('8 - Перейти к показу вакансий и добавлению в список избранного')
            print('0 - Выход')

            user_input = input()

            if user_input == '0':
                self.__call__()
            elif user_input == '1':
                self.all_list.sorting_vacancies_data()
                self.showing_all_list_vacancies()
            elif user_input == '2':
                self.all_list.sorting_vacancies_salary()
                self.showing_all_list_vacancies()
            elif user_input == '3':
                print('Какое слово мы должны использовать для фильтрации?')
                word_filter = input().lower()
                self.all_list.filter_list_word(word_filter)
                self.showing_all_list_vacancies()
            elif user_input == '4':
                print('Какую зарплату нам следует использовать для фильтрации?')
                while True:
                    salary = input()
                    if salary.isdigit():
                        self.all_list.filter_list_salary(int(salary))
                        self.showing_all_list_vacancies()
                        break
                    else:
                        print('Неправильная зарплата')
            elif user_input == '5':
                self.showing_all_list_vacancies()
            elif user_input == '6':
                path = self.all_list.save_csv()
                print(f'Понравившиеся вакансии сохранены в CSV-файле. - {path}')
                self.__call__()
            elif user_input == '7':
                path = self.all_list.save_xlsx()
                print(f'понравившиеся вакансии сохранены в XLSX-файле - {path}')
                self.__call__()
            elif user_input == '8':
                self.showing_all_list_vacancies()
                self.choosing_vacancies_in_my_list()
            else:
                print('Неизвестная команда')

    def showing_all_list_vacancies(self):
        """
        Показать все вакансии
        """
        print(self.all_list)

    def choosing_vacancies_in_my_list(self):
        """
        Выбор понравившихся вакансий. Добавление в список избранного.
        :return:
        """
        while True:
            print('Какие вакансии вы выбираете? Напишите цифры (через пробел, например «1 2 3 4 5»). Вы можете написать «все», чтобы добавить все вакансии в список избранных.')
            numbers_vacancies = input().lower()
            if numbers_vacancies == '0':
                break
            elif numbers_vacancies == 'all':
                for vacancy in self.all_list.vacancy_list:
                    self.mylist.add_vacancy(vacancy)

                self.saving_my_list_vacancies()
            else:
                numbers = []

                numbers_str = numbers_vacancies.split()
                for number_str in numbers_str:
                    if number_str.isdigit():
                        numbers.append(int(number_str))
                if numbers == []:
                    print('Попробуйте еще раз или нажмите 0 для выхода.')
                    continue

                for number in numbers:
                    if self.all_list.get_vacancy(number-1):
                        self.mylist.add_vacancy(self.all_list.get_vacancy(number-1))

                self.saving_my_list_vacancies()

    def saving_my_list_vacancies(self):
        """
        Последнее меню для сохранения вакансий в CSV-файл.
        """
        while True:
            print(f'Мы добавили {len(self.mylist)} вакансий. Мы можем спасти их или провести новые исследования. Выбираем, что нам делать?')
            print('1 - Сохранить понравившиеся вакансии в файле CSV.')
            print('2 - Сохранить понравившиеся вакансии в файле XLSX')
            print('3 - Распечатать мои любимые вакансии')
            print('4 - Новый поиск')
            print('0 - Выход')

            user_input = input()

            if user_input == '0':
                self.__call__()
            elif user_input == '1':
                path = self.mylist.save_csv()
                print(f'Понравившиеся вакансии сохранены в CSV. - {path}')
                self.__call__()
            elif user_input == '2':
                path = self.mylist.save_xlsx()
                print(f'Понравившиеся вакансии сохранены в XLSX - {path}')
                self.__call__()
            elif user_input == '3':
                print(self.mylist)
            elif user_input == '4':
                self.choosing_parameters()
            else:
                print('Неизвестная команда')

    def delete_duplicates(self):
        """
        Функция удаления дубликатов в параметрах
        """
        self.param = {
            'website': list(set(self.param['website'])),
            'city': list(set(self.param['city'])),
            'words': list(set(self.param['words'])),
            'date': self.param['date']
        }