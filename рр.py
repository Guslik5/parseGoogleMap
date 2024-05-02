from selenium import webdriver
from bs4 import BeautifulSoup
import time
import io
import pandas as pd
# добавьте путь к вашему драйверу Chrome здесь
browser = webdriver.Chrome("Путь к вашему драйверу Chrome")# добавьте ссылку на вашу карту Google, данные которой вы хотите спарсить
browser.get('https://www.google.com/maps/place/abc')
browser.maximize_window()
time.sleep(3)
content = browser.find_element_by_class_name('scrollable-show').click()
htmlstring = browser.page_source
afterstring=""
for i in range(12):
    afterstring = htmlstring
    actions.send_keys(Keys.PAGE_DOWN).perform()
    htmlstring = browser.page_source
    if (i>12):
        print ("завершение парсинга, тест номер один")
        actions.send_keys(Keys.PAGE_DOWN).perform()
        htmlstring = browser.page_source
        if (i>12):
           print ("--Конец парсинга--")
           break
    time.sleep(3)
    textdoc = io.open("data.txt", "a+", encoding="utf-8")
soup = BeautifulSoup(htmlstring,"html.parser")
mydivs = soup.findAll("div", {"class": "section-review-content"})
counter = 0
Reviwer_data ={'Имя рецензента':[],'Рейтинг рецензента':[],'URL профиля рецензента':[],'Рецензия':[],'Время':[]}
for a in mydivs:
    textdoc.write(str("\nИмя рецензента: "+a.find("div", class_="section-review-title").text)+" \n||URL профиля рецензента:"+ str(a.find("a").get('href')))
    textdoc.write(" \n||Рецензия:" + a.find("span", class_="section-review-text").text+" \n||Время: " + a.find("span", class_="section-review-publish-date").text)
    textdoc.write("\n")
    textdoc.write(str(a.find("span", class_="section-review-stars")))
    textdoc.write("=========================================\n")
    Reviwer_data['Имя рецензента'].append(a.find("div", class_="section-review-title").text)
    Reviwer_data['Рейтинг рецензента'].append(str(a.find("span", class_="section-review-stars")))
    Reviwer_data['URL профиля рецензента'].append(str(a.find("a").get('href')))
    Reviwer_data['Рецензия'].append(a.find("span", class_="section-review-text").text)
    Reviwer_data['Время'].append(a.find("span", class_="section-review-publish-date").text)
    counter = counter + 1
print("Всего спарсено рецензий:"+str(counter))
textdoc.close()
pd.DataFrame(Reviwer_data).to_csv('data.csv',index=0)