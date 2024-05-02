from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

chromedrive_path = './chromedriver'
driver = webdriver.Chrome()
#driver.get('url')

def parse_real_estate_agencies(keyword, locations):
    base_url = "https://www.google.com/maps/search/"
    results = []


    user_agent = UserAgent()

    for location in locations:
        search_term = f"{keyword} {location}"
        # перекодируем поисковую строку для url
        encoded_search_term = quote(search_term)
        url = f"{base_url}{encoded_search_term}"
        print(f"Формируем URL: {url}")

        headers = {'User-Agent': user_agent.random}
        print(f"Используем User-Agent: {headers['User-Agent']}")



        try:
            response = requests.get(url, headers=headers)

# отправляем get-запрос по указанному url
            print("Статус ответа HTTP:", response.status_code)

# проверка статуса ответа (если ответ = 200, то все ок)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                listings = soup.find_all('.section-result')
                print(f"Найдено {len(listings)} результатов на странице")

                if not listings:
                    print(f"Для запроса '{search_term}' не найдено результатов на странице")
                else:

                    for index, listing in enumerate(listings, start=1):
                        agency_name = listing.find('h3').text
                        website_element = listing.find("div", class_="section-result-details")
                        website = website_element.a["href"] if website_element and website_element.a else "Нет данных"
                        address = listing.find("span", class_="section-result-location").text.strip()
                        phone_element = listing.find("span", class_="section-result-phone-number")
                        phone_number = phone_element.text.strip() if phone_element else "Нет данных"

# Нет прямых способов получения электронной почты из Google Maps
                        print(f"Агентство #{index}")
                        print("Название:", agency_name)
                        print("Адрес:", address)
                        print("Телефон:", phone_number)
                        print()

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

        except Exception as e:
                    print(f"Произошла ошибка: {str(e)}")

    return results

'''
elems = driver.find_elements(By.XPATH, "//div[@role='article']")
for elem in elems:
    title = elem.find_element(By.CSS_SELECTOR, "div.fontHeadlineSmall")
    description = elem.find_element(By.CSS_SELECTOR, "div.fontBodyMedium")
    results.append(str(title.text)+';'+str(description.text))
driver.close()
print(results)

'''