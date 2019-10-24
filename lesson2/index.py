from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['geekbrains']
jobs = db.jobs


def get_jobs(vacancy_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    jobs = []

    hh_link = "https://hh.ru"
    hh_sub_link = f"/search/vacancy?area=1&st=searchVacancy&text={vacancy_name}"
    page_count = 3

    pattern1 = re.compile(r"от ([0-9]+\s[0-9]+) (\w+.)")
    pattern2 = re.compile(r'([0-9]+\s[0-9]+)-([0-9]+\s[0-9]+) (\w+.)')
    pattern3 = re.compile(r'до ([0-9]+\s[0-9]+) (\w+.)')

    while (page_count > 0) and (len(hh_sub_link) > 0):
        req = requests.get(hh_link + hh_sub_link, headers=headers)
        parsed_hh = bs(req.text, 'lxml')

        list = parsed_hh.find("div", {"class": "vacancy-serp"}).findChildren(recursive=False)
        for job in list:
            job_data = {}
            vacancy = job.find("a", {"class": "bloko-link HH-LinkModifier"})
            if vacancy is not None:
                job_data['title'] = vacancy.getText()
                job_data['link'] = vacancy['href']

                price = job.find('div', {'class': 'vacancy-serp-item__compensation'})
                job_data['price_from'] = None
                job_data['price_to'] = None
                job_data['currency'] = ""
                if price is not None:
                    price = price.getText()
                    subs = pattern1.findall(price)
                    if len(subs) > 0:
                        job_data['price_from'] = int(subs[0][0].replace('\xa0', ' ').replace(' ', ''))
                        job_data['currency'] = subs[0][1]
                    else:
                        subs = pattern2.findall(price)
                        if len(subs) > 0:
                            job_data['price_from'] = int(subs[0][0].replace('\xa0', ' ').replace(' ', ''))
                            job_data['price_to'] = int(subs[0][1].replace('\xa0', ' ').replace(' ', ''))
                            job_data['currency'] = subs[0][2]
                        else:
                            subs = pattern3.findall(price)
                            if len(subs) > 0:
                                job_data['price_to'] = int(subs[0][0].replace('\xa0', ' ').replace(' ', ''))
                                job_data['currency'] = subs[0][1]
                            else:
                                print("Не поддерживаемый формат цены!")
                                print(price)

                    job_data['source'] = hh_link

                    jobs.append(job_data)

        hh_sub_link = parsed_hh.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        if hh_sub_link is not None:
            hh_sub_link = hh_sub_link['href']
        else:
            hh_sub_link = ''
        page_count -= 1

    superjob_link = "https://www.superjob.ru"
    superjob_sub_link = f"/vacancy/search/?keywords={vacancy_name}"
    page_count = 3

    while (page_count > 0) and (len(superjob_sub_link) > 0):
        req = requests.get(superjob_link + superjob_sub_link, headers=headers)
        parsed_hh = bs(req.text, 'lxml')

        list = parsed_hh.find("div", {"class": "iJCa5 _1JhPh _2gFpt _1znz6 _1LlO2 _2nteL"}). \
            find('div', {'class': '_3Qutk _2STRT _3ddeP _2ktKi _1DJDo _29NVe'}). \
            find('div', {'class': '_1Ttd8 _2CsQi'}). \
            find('div', {'class': '_1ID8B'}). \
            find('div', {'class': '_3zucV'}).find('div', {'style': 'display:block'}).findChildren('div',
                                                                                                  recursive=False)
        for job in list:
            job_data = {}
            vacancy = job.find("div", {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'})
            if vacancy is not None:
                job_data['title'] = vacancy.getText()
                parent = vacancy.parent
                job_data['link'] = superjob_link + parent['href']

                job_data['price_from'] = None
                job_data['price_to'] = None
                job_data['currency'] = ""

                price = parent.parent.parent.find('span', {
                    'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).findChildren(
                    recursive=False)

                if len(price) == 2:
                    job_data['price_from'] = int(price[0].getText().replace('\xa0', ' ').replace(' ', ''))
                    job_data['currency'] = price[1].getText()
                elif len(price) == 4:
                    job_data['price_from'] = int(price[0].getText().replace('\xa0', ' ').replace(' ', ''))
                    job_data['price_to'] = int(price[2].getText().replace('\xa0', ' ').replace(' ', ''))
                    job_data['currency'] = price[3].getText()

                job_data['source'] = superjob_link
                jobs.append(job_data)

        superjob_sub_link = parsed_hh.find('a',
                                           {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe'})
        if superjob_sub_link is not None:
            superjob_sub_link = superjob_sub_link['href']
        else:
            superjob_sub_link = ''
        page_count -= 1

        return jobs


def save_jobs(result):
    jobs.insert_many(result)


def get_vacancies_gt_price(price):
    return jobs.find({"price_from": {'$gte': price}}).sort('price_from')


if __name__ == '__main__':
    # для упрощения убераю возможность выбрать другую профессию
    # в идеяле нужно было отдельно хранить найденные вакансии по каждой профессии
    vacancy_name = "python"

    result = get_jobs(vacancy_name)
    save_jobs(result)

    price = input('Введите интересующую вас зарплату: ')
    objects = get_vacancies_gt_price(int(price))
    for obj in objects:
        pprint(obj)
