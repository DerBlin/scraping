import requests
from fake_headers import Headers
import bs4
import re
import json
import unicodedata

if __name__ == "__main__":
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )


def generate_headers():
    for i in range(10):
        return(header.generate())


HOST = "https://spb.hh.ru/search/vacancy?L_save_area=true&text=Python+django+flask&excluded_text=&area=2&area=1&sa" \
       "lary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50"

response = requests.get(HOST, headers=generate_headers())
main_html_data = response.text
main_soup = bs4.BeautifulSoup(main_html_data, features='html5lib')
city_list_tag = main_soup.find(name='main', class_='vacancy-serp-content')
group_tag = city_list_tag.find_all('div', 'vacancy-serp-item__layout')
job_list = []
for el in group_tag:
    link = el.find('a')['href']
    reward = el.find('span', class_='bloko-header-section-2')
    if reward is None:
        reward = 'ЗП не указана'
    else:
        reward = reward.text
    company = el.find('a', class_='bloko-link bloko-link_kind-tertiary')
    city = el.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
    job_list.append({
        'link': link,
        'reward': reward.replace('\u202f', ' '),
        'company': company.text,
        'city': city.text
    })


with open('job_list.json',  'w', encoding='utf-8') as file:
    json.dump(job_list, file)
with open('job_list.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
    print(data)
