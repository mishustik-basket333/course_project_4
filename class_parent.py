from abc import ABC, abstractmethod
from pprint import pprint

import requests
import json


PRICE_EUR = 85
PRICE_USD = 80
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
        """Метод делает запрос на https://api.hh.ru/vacancies и возвращает результат в формате json по ключу [items]"""
        headers = {
            "HH-User-Agent": "TestApp/1.0(test@example.com)"
        }

        params = {
            "text": key_name,
            "page": page,
            "per_page": 20,
        }

        return requests.get("https://api.hh.ru/vacancies", params=params).json()["items"]

    def get_vacancies(self, key_name, count=1000):
        """"""
        responce = []
        for i in range(self.Page_count):
            print(f"Парсинг страницы {i + 1}", end=": ")
            values = self.get_request(key_name, i)
            print(f"Найдено {len(values)} вакансий")
            responce.extend(values)
        return responce


class Vacancy:
    """Класс вакансий"""

    #    __slots__ = ("title", "salary_from", "salary_to", "url", "employer_name")
    def __init__(self, title, salary_from, salary_to, salary_currency, url, employer_name, responsibility):
        self.title = title
        self.url = url
        self.employer_name = employer_name
        self.responsibility = responsibility
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
        msg = f"{self.employer_name}  :  {self.title}\n" \
              f"URL вакансии: {self.url} \n" \
              f"{self.salary_currency}{self.salary_from}{self.salary_to}\n" \
              f"Описание обязанностей: {self.responsibility}"
        return msg

    def __gt__(self, other):
        """Метод сравнения"""
        if not other.salary_from:
            return True
        if not self.salary_from:
            return False
        return self.salary_from >= other.salary_from




class JSONSaver:
    """Класс для работы с данными о вакансиях"""

    def __init__(self, key_name: str, name_file: str):
        self.__filename = f"{key_name.title()}_{name_file.lower()}.json"

    @property
    def filename(self):
        return self.__filename

    def add_vacancy(self, data):
        """Добавляет вакансии в файл 'self.__filename'"""
        with open(self.__filename, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self):
        vacansies = []
        salary_from, salary_to, salary_currency = None, None, None

        with open(self.__filename, "r", encoding="UTF-8") as file:
            data = json.load(file)

        if "hh" in self.filename:

            for row in data:
                # salary_from, salary_to, salary_currency = None, None, None
                if row["salary"]:
                    salary_from, salary_to, salary_currency = row["salary"]["from"], row["salary"]["to"], row["salary"][
                        "currency"]
                    if row["salary"]["currency"].upper() == "EUR":
                        salary_from = row["salary"]["from"]*PRICE_EUR
                        salary_to = row["salary"]["to"] * PRICE_EUR
                        salary_currency = "RUR"
                    if row["salary"]["currency"].upper() == "USD":
                        salary_from = row["salary"]["from"]*PRICE_USD
                        salary_to = row["salary"]["to"] * PRICE_USD
                        salary_currency = "RUR"

                vacansies.append(Vacancy(
                    row["name"],
                    salary_from,
                    salary_to,
                    salary_currency,
                    row["alternate_url"],
                    row["employer"]["name"],
                    row["snippet"]["responsibility"]))

        if "sj" in self.filename:

            for row in data:
                if row["currency"]:
                    salary_from, salary_to, salary_currency = row["payment_from"], row["payment_to"], row["currency"]

                    if row["currency"].upper() == "EUR":
                        salary_from = row["payment_from"]*PRICE_EUR
                        salary_to = row["payment_to"] * PRICE_EUR
                        salary_currency = "RUR"
                    if row["currency"].upper == "USD":
                        salary_from = row["payment_from"]*PRICE_USD
                        salary_to = row["payment_to"] * PRICE_USD
                        salary_currency = "RUR"

                vacansies.append(Vacancy(
                    row["profession"],
                    salary_from,
                    salary_to,
                    salary_currency,
                    row["link"],
                    row["firm_name"],
                    row["candidat"]))
                    # "обящанности"))


        return vacansies

def sort_from_minimum_salary(data, reverse_data = False):
    """Функция сортировки по минимальной зарплате, если она не указана, то вакансия пишется в начале списка
     и далее по возрастанию минимальной зарплаты.
     Второй аргумент по умолчанию False, если задать True, то вывод будет обратный"""
    data = sorted(data, reverse=reverse_data)
    return data




if __name__ == "__main__":
    key_name = "python"
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(key_name)
    json_saver = JSONSaver(key_name, "head hunter")
    json_saver.add_vacancy(hh_vacancies)
    print("")
    print("")
    vacansies = json_saver.select()
    sort_vacansies = sort_from_minimum_salary(vacansies, True)
    for row in sort_vacansies:
        print(row)
        print("")
        print("=" * 100)
        print("")
    print("the end")


