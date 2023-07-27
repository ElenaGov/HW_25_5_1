import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()


@pytest.fixture(scope='class', autouse=True)
def enter_to_page():
    # Переходим на страницу авторизации
    driver.get('http://petfriends.skillfactory.ru/login')
    # добавляем ожидание появления кнопки войти
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[@type="submit"]')))
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('elena-3@mail.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('njgfp333**')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    yield

    driver.quit()


class TestPetsFriends:

    def test1_my_pets(self):
	# Присутствуют все питомцы на странице пользователя
        element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="all_my_pets"]')))
        statistics = driver.find_element(By.CSS_SELECTOR, 'div.task3 div')
        number = statistics.text.split(': ')
        st_number = int(number[1][0])
        pets_number = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets .table tbody tr')
        assert len(pets_number) == st_number

    def test2_part_photos(self):
	# Хотя бы у половины питомцев есть фото на странице пользователя
        element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]/h2')))
        photos = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')
        statistics = driver.find_element(By.CSS_SELECTOR, 'div.task3 div')
        number = statistics.text.split(': ')
        number_half = int(number[1][0]) / 2
        count = 0
        for i in range(len(photos)):
            if photos[i].get_attribute('src') != '':
                count += 1
        assert count >= number_half

    def test3_pets_data(self):
	# У всех питомцев есть имя, возраст и порода на странице пользователя 
        driver.implicitly_wait(5)
        pets_data = driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')
        for i in range(len(pets_data)):
            pets_data_part = pets_data[i].text.split(' ')
            assert len(pets_data_part) == 3
            
    def test4_no_duplicate_names(self):
    # У всех питомцев разные имена на странице пользователя 
        driver.implicitly_wait(5)
        pets_data = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[1]')
        pet_name = []
        for i in range(len(pets_data)):
            pets_data_part = pets_data[i].text
            pet_name.append(pets_data_part.split("\n")[0])
        for i in range(len(pet_name) - 1):
            for j in range(i+1, len(pet_name)):
                assert pet_name[i] != pet_name[j]

    def test5_no_duplicate_pets(self):
    # В списке нет повторяющихся питомцев (это питомцы, у которых одинаковое имя, порода и возраст) на странице пользователя
        driver.implicitly_wait(5)
        descriptions = driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets table tbody tr')
        animal_data = []
        for i in range(len(descriptions)):
            animal_data.append(descriptions[i].text.split("\n")[0])
        for i in range(len(animal_data) - 1):
            for j in range(i+1, len(animal_data)):
                assert animal_data[i] != animal_data[j]