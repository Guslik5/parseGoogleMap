import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import os


def parse_real_estate_agencies(keyword, locations):
    results = []
    '''
    их 139
    # Инициализация WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в безголовом режиме (без отображения браузера)
    #service = Service(' /Users/deadbadunicorn/Desktop/agent/chromedriver ')  # Укажите путь к chromedriver
    service = Service(' C:/Users/Guslik/Desktop/chrome-win64')
привет как дела вивиан чем ты занят что нового
    driver = webdriver.Chrome(service=service, options=chrome_options)'''
    options = Options()
    options.add_argument("--start-maximized")
    # TODO: не забыть поставить адрес на винде
    service = Service('')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    print(driver)

    try:
        while True:
                for location in locations:
                    search_term = f"{keyword} {location}"
                    search_url = f"https://www.google.com/maps/search/{search_term}"
                    print("||||||||||||||||||||||||||||||||||||||||||||")
                    print(location)
                    print(driver.get(search_url))
                    driver.get(search_url)
                    time.sleep(2)  # Пауза для загрузки страницы

                    # Ожидание появления результатов поиска
                    wait = WebDriverWait(driver, 100)
                    # element = driver.find_elements(By.CLASS_NAME, "hfpxzc")
                    # print(element)

                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc")))
                    # Получение списка всех элементов с результатами поиска
                    listings = driver.find_elements(By.CLASS_NAME, "hfpxzc")
                    listings2 = driver.find_elements(By.CLASS_NAME, "UsdlK")
                    #listings3 = driver.find_elements(By.CLASS_NAME, "lcr4fdS9kvJb")
                    listings3 = driver.find_elements(By.CSS_SELECTOR, "a.lcr4fd.S9kvJb")
                    #listings3 = driver.find_elements(By.CLASS_NAME, "Rwjeuc")

                   # listings3 = driver.find_elements(By.XPATH, "//div[@class='W4Efsd']//span[2]/span[2]")
                    # for k in range(len(listings3)):
                    #     if k % 2 == 0:
                    #         print(f"adress: {listings3[k].text}")
                    #     else:
                    #         print(f"phone: {listings3[k].text}")
                        # print(f"id :{listings3[k].id} \n text: {listings3[k].text} \n tag_name: {listings3[k].tag_name} \n parent: {listings3[k].parent} \n size {listings3[k].size} \n")
                    for i in range(len(listings)):
                        title = listings[i].get_attribute("aria-label")
                        phone = listings2[i].text
                        # address = listings2[i].find_element(By.XPATH, "//div[@class='W4Efsd']//span[2]/span[2]").text
                        # address = listings3[i].find_element(By.TAG_NAME, "span").text
                        # address = listings3[i].find_element(By.XPATH, "//span[2]/span[2]").text
                        #website_url = listings3[i].get_attribute("href")

                        try:
                         website_url = listings3[i].get_attribute("href")
                         #print(website_url)
                        except NoSuchElementException:
                            website_url = "No web"
                            print("Нет ссылки на сайт")

                        #address = listings3[i*2].text
                       # phone = listings3[i*2+1].text
                        print("================================================================")
                        print(f"Название: {title}")
                        print(f"Ссылка на сайт: {website_url}")
                        print(f"Телефон:{phone}")
                        """
                        магическое число i*2 тк структура внутри html имеет 2 одинаковых структуры 
                        "//div[@class='W4Efsd']//span[2]/span[2]" одну для номера и одну для адреса
                        они располагаются в четном/нечетном порядке(четный-адрес, нечетный-номер)
                        """
                       # print(f"Адрес: {listings3[i*2].text}")
                        #print(f"Телефон: {listings3[i*2+1].text}")
                        #для адреса вот класс W4Efsd

                        results.append({
                            "Страна": location,
                            "Название": title,
                            "Телефон": phone,
                            "Ссылка на сайт": website_url
                         })
                        # driver.execute_script("window.scrollTo(1000, document.body.scrollHeight);")
                        # Если есть кнопка перехода на следующую страницу, то продолжаем цикл, иначе завершаем
    #return results
    finally:
        driver.quit()  # Закрытие WebDriver после завершения парсинга
    return results

if __name__ == "__main__":
    keyword = "агентство недвижимости"
    locations = ["ОАЭ"]

    #locations = ["ОАЭ", "Таиланд", "Турция", "Бали", "Кипр"]

    try:
        print(f"Выполняется парсинг данных для запроса: '{keyword}'...")
        parsed_data = parse_real_estate_agencies(keyword, locations)

        if parsed_data:
            # Сохранение данных в файл Excel
            df = pd.DataFrame(parsed_data)
            print(df)
            # if os.path.exists('real_estate_agencies.xlsx'):
            #     os.remove('real_estate_agencies.xlsx')
            #
            # print(os.path.exists('real_estate_agencies.xlsx'))
            df.to_excel('real_estate_agencies.xlsx', index=False)
            print("Данные успешно сохранены в файл 'real_estate_agencies.xlsx'")
        else:
            print("Не удалось найти результаты для запроса")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")