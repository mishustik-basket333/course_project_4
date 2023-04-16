from abc import ABC, abstractmethod
from functions import *
from global_variables import *

import requests
import json


class ParentApiClass(ABC):
    """Родительский класс, для классов, которые работают с API"""

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(ParentApiClass):
    """Класс для работы с API Head Hunter"""

    def get_request(self, key_word, page):
        """Метод делает запрос на https://api.hh.ru/vacancies и возвращает результат в формате json по ключу [items]"""
        params = {
            "text": key_word,
            "page": page,
            "per_page": VACANCY_COUNT,
        }
        return requests.get("https://api.hh.ru/vacancies", params=params).json()["items"]

    def get_vacancies(self, key_word):
        """Функция получает список заданных вакансию по кодовому слову и возвращает его"""
        data_list = []
        for x in range(PAGE_COUNT):
            values = self.get_request(key_word, x)
            data_list.extend(values)
        return data_list


class SuperJobAPI(ParentApiClass):
    """Класс для взаимодейстивя с SuperJobAPI"""
    page_count = 2

    def get_request(self, key_word, page):
        auth_data = {'X-Api-App-Id': key_job}
        params = {
            "keyword": key_word,
            "page": page,
            "count": VACANCY_COUNT,
        }
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=auth_data, params=params).json()[
            "objects"]
        return response

    def get_vacancies(self, key_word):
        """Функция получает список заданных вакансию по кодовому слову и возвращает его"""
        data_list = []
        for x in range(PAGE_COUNT):
            values = self.get_request(key_word, x)
            data_list.extend(values)
        return data_list


class Vacancy:
    """Класс вакансий"""
    def __init__(self, title, salary_from, salary_to, salary_currency, url, employer_name, address):
        self.title = title
        self.url = url
        self.employer_name = employer_name
        self.address = address
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency

    def __str__(self):
        if self.salary_currency:
            self.salary_currency = f"Зарплата({self.salary_currency}) "
        else:
            self.salary_currency = "Зарплата не указана"
        if self.salary_from:
            self.salary_from = f"от:{self.salary_from}  "
        else:
            self.salary_from = ""
        if self.salary_to:
            self.salary_to = f"до:{self.salary_to}"
        else:
            self.salary_to = " "
        if not self.address:
            self.address = "Не указано"
        msg = f"{self.employer_name}  :  {self.title}\n" \
              f"URL вакансии: {self.url} \n" \
              f"{self.salary_currency}{self.salary_from}{self.salary_to}\n" \
              f"Адрес работодателя: {self.address}"
        return msg

    def __gt__(self, other):
        """Метод сравнения по минимальной зарплате"""
        if not other.salary_from:
            return True
        if not self.salary_from:
            return False
        return self.salary_from >= other.salary_from


class JSONSaver:
    """Класс для работы с данными о вакансиях"""
    def __init__(self, key_word: str, name_file: str):
        self.__filename = f"{key_word.title()}_{name_file.lower()}.json"

    @property
    def filename(self):
        return self.__filename

    def add_vacancy(self, data):
        """Добавляет вакансии в файл 'self.__filename'"""
        with open(self.__filename, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self):
        """Функция создает экземпляры класса Vacancy с заданными полями.
         Если указана запралата, то пересчитываёт её в рубли(при необходимости)
         Возвращает список вакансий
         """
        vacansies_list = []
        salary_from, salary_to, salary_currency = None, None, None

        with open(self.__filename, "r", encoding="UTF-8") as file:
            data = json.load(file)

        if "hh" in self.filename:
            for row in data:
                if row["salary"] and row["salary"]["to"] and row["salary"]["from"]:
                    salary_from, salary_to, salary_currency = row["salary"]["from"], row["salary"]["to"], row["salary"][
                        "currency"]
                    if row["salary"]["currency"].upper() == "EUR":
                        salary_from = row["salary"]["from"] * PRICE_EUR
                        salary_to = row["salary"]["to"] * PRICE_EUR
                    if row["salary"]["currency"].upper() == "USD":
                        salary_from = row["salary"]["from"] * PRICE_USD
                        salary_to = row["salary"]["to"] * PRICE_USD
                    salary_currency = "RUB"

                vacansies_list.append(Vacancy(
                    row["name"],
                    salary_from,
                    salary_to,
                    salary_currency,
                    row["alternate_url"],
                    row["employer"]["name"],
                    row["area"]["name"]))

        if "sj" in self.filename:
            for row in data:
                if row["currency"]:
                    salary_from, salary_to, salary_currency = row["payment_from"], row["payment_to"], row["currency"]

                    if row["currency"].upper() == "EUR":
                        salary_from = row["payment_from"] * PRICE_EUR
                        salary_to = row["payment_to"] * PRICE_EUR
                    if row["currency"].upper == "USD":
                        salary_from = row["payment_from"] * PRICE_USD
                        salary_to = row["payment_to"] * PRICE_USD
                    salary_currency = "RUB"

                vacansies_list.append(Vacancy(
                    row["profession"],
                    salary_from,
                    salary_to,
                    salary_currency,
                    row["link"],
                    row["firm_name"],
                    row["address"]))

        return vacansies_list

#
# if __name__ == "__main__":
#     key_name = "python developer"
#     superjob_api = SuperJobAPI()
#     sj_vacancies = superjob_api.get_vacancies(key_name)
#     json_saver = JSONSaver(key_name, "SJ")
#     json_saver.add_vacancy(sj_vacancies)
#     vacansies = json_saver.select()
#
#     sort_vacansies = get_vacancies_by_salary(vacansies, 40_000)
#     sort_vacansies = sort_from_minimum_salary(sort_vacansies, True)
#     top_vacs = get_top_vacancies(sort_vacansies, 5)
#
#     for i in top_vacs:
#         print(i)
#         print("\n", "=" * 100, "\n")
#     print("\n\n", '*' * 100, "\n\n", "the end")
#     print(len(top_vacs))

    # if __name__ == "__main__":
    #     key_name = "python developer"
    #     hh_api = HeadHunterAPI()
    #     hh_vacancies = hh_api.get_vacancies(key_name)
    #     json_saver = JSONSaver(key_name, "HH")
    #     json_saver.add_vacancy(hh_vacancies)
    #     print("")
    #     print("")
    #     vacansies = json_saver.select()
    #     sort_vacansies = sort_from_minimum_salary(vacansies, True)
    #     # sort_vacansies = get_vacancies_by_salary(vacansies, 40000, 600000)
    #     for row in sort_vacansies:
    #         print(row)
    #         print("")
    #         print("=" * 100)
    #         print("")
    #     print("the end")
    #     print(len(sort_vacansies))
