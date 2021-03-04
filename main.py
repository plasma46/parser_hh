import requests
from bs4 import BeautifulSoup
import datetime
import csv


timestamp = datetime.datetime.now()

CSV = 'vacancy.csv'
HOST = 'https://kursk.hh.ru/'
URL = 'https://kursk.hh.ru/catalog/Informacionnye-tehnologii-Internet-Telekom'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(URL, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all(class_='vacancy-serp-item')
    vacancy = []
    for item in items:
        try:
            vacancy.append(
                {'name': item.find(class_='bloko-link').get_text(),
                 'salary': item.find('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite',
                                              'data-qa': 'vacancy-serp__vacancy-compensation'}),
                 'company': item.find(class_='bloko-link bloko-link_secondary').get_text(strip=True),
                 'link': item.find(class_='bloko-link HH-LinkModifier HH-VacancyActivityAnalytics-Vacancy').attrs[
                     'href'],
                 'opis': item.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).get_text(
                     strip=True),
                 'treb': item.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).get_text(
                     strip=True),
                 'date': item.find('span', 'vacancy-serp-item__publication-date').get_text(),
                 'timestamp': timestamp
                 }
            )
        except AttributeError :
            continue

    # , 'data-qa': 'vacancy-serp__vacancy-employer'})
    return vacancy


# html = get_html(URL)
#
# new = get_content(html.text)

# hh = {}
# for dic in new:
#     for key,value in dic.items():
#         if key == 'name':
#             hh['name'] = value
#         if key == 'salary' and value is not None:
#             hh['samary'] = value.replace_with('')
#         else:
#             hh['samary'] = ''


# for g in new:
#     print(g)
def save_csv (items):
    with open('vacancy.csv',mode='w+',newline='',encoding='cp1251',errors='ignore') as file:
        writer = csv.writer(file,delimiter =';')
        writer.writerow(['Должность','ЗП','Компания','ссылка'
                            ,'Описание','Требование','Дата обновления','метка'])
        for item in items:
            try:
                writer.writerow([item['name'], item['salary'].get_text(strip=True), item['company'], item['link']
                                , item['opis'], item['treb'], item['date'], item['timestamp']])
            except AttributeError :
                writer.writerow([item['name'],'Не указана', item['company'], item['link']
                                    , item['opis'], item['treb'], item['date'], item['timestamp']])




def parser():
    html = get_html(URL)
    if html.status_code == 200:
        print('fgh')
        vacancy = []
        for page in range(0, 8):
            print(f'Парсим страницу {page}')
            html = get_html(URL, params={'page': page})
            vacancy.extend(get_content(html.text))
            save_csv(vacancy)
        print('Готово')


    else:
        print('Ошибка подключения')
    return vacancy

parser()


#     if key == 'salary':
#         if key is not None:
#             new['salary'] = new['salary'].get_text()
#     print(key)
#
#
# for dic in a:
#     for key, value in dic.items():
#         if key == "bag" and value == ["no"]:
#             print(dic)
#             break
#
#
#
#
# for key in new[:]['salary']:
#     if key == 'salary':
#         if key is not None:
#             new['salary'] = new['salary'].get_text()
#     print(key)
