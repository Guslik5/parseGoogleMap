from selenium import webdriver
from bs4 import BeautifulSoup
import time
import io
import json
import xlsxwriter
import pandas as pd
import requests
import re
from selenium.webdriver.chrome.options import Options

# для запуска безэкранного браузера Chrome, удобного для парсинга, с использованием Selenium
# BeautifulSoup для анализа содержимого страницы результатов и извлечения данных о компаниях

# запускаем безэкранный браузер Chrome

webdriver.Chrome('')


# отправляем запрос на получение данных с карты и получаем результаты
search_term = "pizza restaurants in Moscow"
search_url = f"https://www.google.com/maps/search/{search_term}"

response = requests.get(search_url)
page_content = response.text

# теперь анализируем данные
soup = BeautifulSoup(page_content, 'html.parser')

for result in soup.select('.section-result'):

  title = result.h3.text
  address = result.find('span', 'address').text

  try:
    rating = result.find('span', 'cards-rating-score').text
  except AttributeError:
    rating = None

  print(title, address, rating )

# также нужно парсить все страницы (то есть нужно обработать нумерацию страниц)

for page in range(1, 10):

  url = f"{search_url}/p{page}"



# Следующая страница
  next_page = soup.find('a', string=re.compile(r'Next'))

  if not next_page:
    break

print('Очистка завершена!')

# Мы циклически увеличиваем номера страниц, очищая каждую страницу, пока ссылка «Далее» больше не будет найдена в супе.
# Это позволяет нам просматривать все доступные страницы и результаты.




all_records = []

for page in range(1, 10):

# Scrape page
# Extract data into dicts

  for result in all_records:
    record = {
    'title': result['title'],
    'address': result['address'],
    'url': result['url']
    }

    all_records.append(record)

# преобразуем данные
#   df = pd.DataFrame(all_records)
# df.to_xlsx('google_maps_data.xlsx', index = False)

