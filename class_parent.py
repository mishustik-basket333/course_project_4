from abc import ABC, abstractmethod
from pprint import pprint

import requests
import json


class ParentClass(ABC):
    """Родительский класс, для классов, которые работают с API"""

    def get_request(self):
        pass

    def get_vacancies(self):
        pass


class HeadHunterAPI(ParentClass):
    """Класс для работы с API Head Hunter"""

    Page_count = 2

    def get_request(self, key_name, page):
        """Метод делает запрос на https://api.hh.ru/vacancies и возвращает результат в формате json по ключу [tems]"""
        headers = {
            "HH-User-Agent": "TestApp/1.0(test@example.com)"
        }

        params = {
            "text": key_name,
            "page": page,
            "per_page": 20,
        }

        return requests.get("https://api.hh.ru/vacancies", params=params, ).json()["items"]

    def get_vacancies(self, key_name, count=1000):
        """"""
        responce = []
        for i in range(self.Page_count):
            print(f"Парсинг страницы {i+1}", end=": ")
            values = self.get_request(key_name, i)
            print(f"Найдено {len(values)} вакансий")
            responce.extend(values)
            # for i in range(self.Page_count):
            #     print(i)
            #     values = self.get_request(key_name, i)
            #     # pprint(values)
            #     # print(len(values))
            #     for raw in values:
            #         print(f'Название вакансии: {raw["name"]}')
            #         print("="*20)
        return responce

class Vacancy:
    """Класс вакансий"""
#    __slots__ = ("title", "salary_from", "salary_to", "url", "employer_name")
    def __init__(self, title, salary_from, salary_to, salary_currency, url, employer_name, responsibility):
        self.title = title
        self.url = url
        self.employer_name = employer_name
        self.responsibility = responsibility
        if salary_currency:
            self.salary_currency = f"Зарплата({salary_currency})"
        else:
            self.salary_currency = "Зарплата не указана"
        if salary_from:
            self.salary_from = f" от: {salary_from}"
        else:
            self.salary_from = " "
        if salary_to:
            self.salary_to = f"   до: {salary_to}"
        else:
            self.salary_to = " "


    def __str__(self):
        msg = f"{self.employer_name}  :  {self.title}\n" \
              f"URL: {self.url} \n" \
              f"{self.salary_currency}{self.salary_from}{self.salary_to}\n" \
              f"Описание обязанностей: {self.responsibility}"
        return msg


class JSONSaver:
    """Класс для работы с данными о вакансиях"""
    def __init__(self, key_name: str):
        self.__filename = f"{key_name.title()}_HH.json"

    @property
    def filename(self):
        return self.__filename

    def add_vacancy(self, data):
        """Добавляет вакансии в файл 'self.__filename'"""
        with open(self.__filename, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self):
        with open(self.__filename, "r", encoding="UTF-8") as file:
            data = json.load(file)

        vacansies = []

        for row in data:
            salary_from, salary_to, salary_currency = None, None, None
            if row["salary"]:
                salary_from, salary_to, salary_currency = row["salary"]["from"], row["salary"]["to"], row["salary"]["currency"]
            vacansies.append(Vacancy(
                row["name"],
                salary_from,
                salary_to,
                salary_currency,
                row["alternate_url"],
                row["employer"]["name"],
                row["snippet"]["responsibility"]))
        # print(vacansies[0])
        return vacansies






key_name = "python"
hh_api = HeadHunterAPI()
hh_vacancies = hh_api.get_vacancies(key_name)
json_saver = JSONSaver(key_name)
json_saver.add_vacancy(hh_vacancies)
print("")
print("")
data = json_saver.select()
for row in data:
    print(row)
    print("")
    print("="*100)
    print("")
print("the end")



