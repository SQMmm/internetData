from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome('./chromedriver')

driver.get('http://geekbrains.ru/login')
assert "GeekBrains" in driver.title

elem = driver.find_element_by_id('user_email')
elem.send_keys(input("user: "))

elem = driver.find_element_by_id('user_password')
elem.send_keys(input("password: "))
elem.send_keys(Keys.RETURN)

profile = driver.find_element_by_class_name("avatar")
driver.get(profile.get_attribute('href'))
assert "Профиль | GeekBrains" in driver.title

edit_profile = driver.find_element_by_class_name('text-sm')
driver.get(edit_profile.get_attribute('href'))
assert "Настройки профиля" in driver.title

gender = driver.find_element_by_name('user[gender]')
# options = gender.find_elements_by_tag_name('option')
# for option in options:
#     if option.text == 'Не выбран':
#         option.click()

select = Select(gender)
select.select_by_value("0")

gender.submit()
