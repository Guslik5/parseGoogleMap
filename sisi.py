import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from fake_useragent import UserAgent
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
# Запускаем безэкранный браузер Chrome для парсинга с помощью Selenium
  webdriver.Chrome(' ')

def parse_real_estate_agencies(keyword, locations):
    base_url = "https://www.google.com/maps/search/"
    results = []

# Генерация случайного User-Agent для каждого запроса (ОБХОД ЗАЩИТЫ)
    user_agent = UserAgent()

    for location in locations:
        search_term = f"{keyword} {location}"
# перекодируем поисковую строку для url
        encoded_search_term = quote(search_term)
        url = f"{base_url}{encoded_search_term}"
        print(f"Формируем URL: {url}")

        headers = {'User-Agent': user_agent.random}
        #print(f"Используем User-Agent: {headers['User-Agent']}")

        try:
            response = requests.get(url, headers=headers)

# отправляем get-запрос по указанному url
           # print("Статус ответа HTTP:", response.status_code)

# проверка статуса ответа (если ответ = 200, то все ок)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                #listings = soup.find_all("div", class_="LoJzbe keynav-mode-off highres screen-mode")
                listings = soup.find_all("div", class_="hfpxzc")
                print(f"Найдено {len(listings)} результатов на странице")

                if not listings:
                    print(f"Для запроса '{search_term}' не найдено результатов на странице")
                else:

                    for index, listing in enumerate(listings, start=1):
                        agency_name = listing.find("h3", class_="aria-label").text.strip()
                        website_element = listing.find("div", class_="W4Efsd")
                        website = website_element.a["href"] if website_element and website_element.a else "Нет данных"
                        address = listing.find("span", class_="W4Efsd").text.strip()
                        phone_element = listing.find("span", class_="UsdlK-")
                        phone_number = phone_element.text.strip() if phone_element else "Нет данных"

# Нет прямых способов получения электронной почты из Google Maps
                       # print(f"Агентство #{index}")
                        #print("Название:", agency_name)
                       # print("Адрес:", address)
                       # print("Телефон:", phone_number)
                       # print()

# Сохраняем результаты в список словарей
                        results.append({
                            "№ п/п": index,
                            "Название": agency_name,
                            "Сайт": website,
                            "Адрес": address,
                            "Номер телефона": phone_number,
                         })
# задержка перед следующим запросом
                        time.sleep(1)

            else:
                print(f"Ошибка при запросе к URL: {url}")

# Вывод содержимого ответа для отладки
                print(f"Содержимое ответа: {response.content}")

        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при выполнении запроса: {str(e)}")

    return results

# Сохранение и перенос в эксель
def save_to_excel(data, filename):
    try:
        # Преобразуем список словарей в DataFrame с помощью pandas
        df = pd.DataFrame(data)
        print(df)
        # Сохраняем DataFrame в файл Excel
        df.to_excel(filename, index=False)

        print(f"Данные успешно сохранены в файл Excel: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении данных в Excel: {str(e)}")




if __name__ == "__main__":
    keyword = "агентство недвижимости"
    locations = ["ОАЭ", "Таиланд", "Турция", "Бали", "Кипр"]

    try:
        print(f"Выполняется парсинг данных для запроса: '{keyword}'...")
        parsed_data = parse_real_estate_agencies(keyword, locations)

        # Сохраняем данные в файл Excel
        save_to_excel(parsed_data, 'real_estate_agencies.xlsx')

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
