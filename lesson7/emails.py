from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas

driver = webdriver.Chrome('./chromedriver')
driver.get('https://mail.google.com')

assert "Gmail" in driver.title
elem = driver.find_element_by_id('identifierId')

elem.send_keys(input('Email: '))
elem.send_keys(Keys.RETURN)

elem = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.NAME, 'password'))
)

elem.send_keys(input("Password: "))
elem.send_keys(Keys.RETURN)

time.sleep(4)

assert "Входящие" in driver.title
driver.find_element_by_id(':2c').click()

items = []

while True:
    try:
        # находим письма из вкладки "Промоакции"
        tab = driver.find_elements_by_class_name('ae4.aDM')[2]
        # отбрасываем рекламу
        table = tab.find_elements_by_class_name('Cp')[1]
        emails = table.find_elements_by_tag_name('tr')

        for email in emails:
            # переходим в письмо
            email.click()
            time.sleep(0.5)

            sender = driver.find_element_by_class_name('gD').text
            title = driver.find_element_by_class_name('hP').text
            date = driver.find_element_by_class_name('g3').get_attribute('title')
            text = driver.find_element_by_class_name('ii.gt').text

            items.append({
                'sender': sender,
                'title': title,
                'date': date,
                'text': text
            })

            # возвращаемся обратно в список
            driver.back()

        driver.find_element_by_id(':3q').click()

    except Exception as e:
        print(e)
        break

result = pandas.DataFrame(items)
print(result.head())

driver.quit()
