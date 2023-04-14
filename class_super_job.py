from class_parent import *
import requests
import json

key_job = "v3.r.137483720.787d25efef2944db00ee9f886f29e554297a5864.572b1f3347d6d3fe8b7962d6715b0bae18bafa3d"


class SuperJobAPI(ParentClass):
    """Класс для взаимодейстивя с SuperJobAPI"""

    Page_count = 2

    def get_request(self, key_name, page):

        auth_data = {'X-Api-App-Id': key_job}
        params = {
                "keyword": key_name,
                "page": page,
                "count": 20,
        }
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=auth_data, params=params).json()["objects"]
        return response

    def get_vacancies(self, key_name):
        """"""
        responce = []
        for i in range(self.Page_count):
            print(f"Парсинг страницы {i + 1}", end=": ")
            values = self.get_request(key_name, i)
            print(f"Найдено {len(values)} вакансий")
            responce.extend(values)
        return responce


if __name__ == "__main__":

    key_name = "python"

    superjob_api = SuperJobAPI()
    sj_vacancies = superjob_api.get_vacancies(key_name)
    json_saver = JSONSaver(key_name, "SJ")
    json_saver.add_vacancy(sj_vacancies)

    # for row in sj_vacancies:
    #     print("="*100)
    #     print(row['profession'])
    #     print(row['link'])
    #
    # print("111")

    vacansies = json_saver.select()

    for i in vacansies:
        print(i)
        print("\n", "="*100,  "\n")

    print("\n\n", '*'*100, "\n\n", "the end")
