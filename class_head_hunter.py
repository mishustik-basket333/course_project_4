from class_parent import *
import requests
import json

PRICE_EUR = 85
PRICE_USD = 80

class HeadHunterAPI(ParentClass):
    """Класс для работы с API Head Hunter"""

    Page_count = 2

    def get_request(self, key_name, page):
        """Метод делает запрос на https://api.hh.ru/vacancies и возвращает результат в формате json по ключу [items]"""
        # headers = {"HH-User-Agent": "TestApp/1.0(test@example.com)"}

        params = {
            "text": key_name,
            "page": page,
            "per_page": 20,
        }

        return requests.get("https://api.hh.ru/vacancies", params=params).json()["items"]

    def get_vacancies(self, key_name):
        """"""
        responce = []
        for i in range(self.Page_count):
            print(f"Парсинг страницы {i + 1}", end=": ")
            values = self.get_request(key_name, i)
            print(f"Найдено {len(values)} вакансий")
            responce.extend(values)
        return responce


# if __name__ == "__main__":
#     key_name = "python developer"
#     hh_api = HeadHunterAPI()
#     hh_vacancies = hh_api.get_vacancies(key_name)
#     json_saver = JSONSaver(key_name, "head_hunter")
#     json_saver.add_vacancy(hh_vacancies)
#     print("")
#     print("")
#     vacansies = json_saver.select()
#     sort_vacansies = sort_from_minimum_salary(vacansies, True)
#     for row in sort_vacansies:
#         print(row)
#         print("")
#         print("=" * 100)
#         print("")
#     print("the end")
if __name__ == "__main__":
    key_name = "python"
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(key_name)
    json_saver = JSONSaver(key_name, "HH")
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
