import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math


@pytest.fixture(autouse=True)
def testing():
    """Фикстура для прохождения авторизации"""
    pytest.driver = webdriver.Edge('.\msedgedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/login')
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('ldarovskaya@yandex.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('173asd')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Переход на страницу - Мои питомцы
    pytest.driver.implicitly_wait(10)
    pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    my_pets_names = pytest.driver.find_elements(By.XPATH, '//tr/td[1]')
    my_pets_animal_types = pytest.driver.find_elements(By.XPATH, '//tr/td[2]')
    my_pets_ages = pytest.driver.find_elements(By.XPATH, '//tr/td[3]')
    my_pets_images = pytest.driver.find_elements(By.XPATH, '//tr//img')

    yield

    pytest.driver.quit()

#Написать тест, который проверяет, что на странице со списком питомцев пользователя:
#1) Присутствуют все питомцы.
def test_count_my_pets():
    """Проверяем, что кол-во строк в таблице со своими питомцами совпадает
        с количеством из статистики пользователя"""
    #Количество питомцев(строк) в таблице посчитаем равным
    #количеству крестиков для их удаления
    #явное ожидание отображения элементов на странице
    my_pets = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'td.smart_cell')))
    #my_pets = pytest.driver.find_elements(By.CSS_SELECTOR,'td.smart_cell')


    #находим блок с информацией о кол-ве питомцев
    # явное ожидание отображения элементов на странице
    statistic_of_user_pets = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[@class=".col-sm-4 left"]')))
    #statistic_of_user_pets = pytest.driver.find_element(By.XPATH,'//div[@class=".col-sm-4 left"]')
    #обрабатываем строку -> переводим в список, элемент с индексом 2 является искомым кол-вом питомцев
    list_with_user_data=statistic_of_user_pets.text.replace('\n',': ').split(': ')

    #подсчет кол-ва питомцев в таблице
    count_of_pets=0
    for i in range(len(my_pets)):
        count_of_pets+=1

    assert int(list_with_user_data[2]) == count_of_pets

#2)Хотя бы у половины питомцев есть фото.
def test_half_part_of_pets_has_photo():
    """Проверка, что хотя бы у половины питомцев пользователя есть фото
     - сравнение с кол-вом питомцев из статистики пользователя"""
    # находим блок с информацией о кол-ве питомцев
    #явное ожидание элемента на странице
    statistic_of_user_pets = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))
    #statistic_of_user_pets = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]')
    # обрабатываем строку -> переводим в список, элемент с индексом 2 является искомым кол-вом питомцев
    list_with_user_data = statistic_of_user_pets.text.replace('\n', ': ').split(': ')
    #получим список фото питомцев
    my_pets_images=pytest.driver.find_elements(By.XPATH,'//tr//img')

    #считаем кол-во питомцев у которых есть фото
    count_of_image=0
    for i in range(len(my_pets_images)):
        if my_pets_images[i].get_attribute('src') != '':
            count_of_image+=1

    #сравниваем что кол-во питомцев с фото >= половине кол-ва питомцев
    #использована функция math.ceil для верного округления ситуаций с делением нечетных чисел (деление на 2, здесь допустимо)
    assert count_of_image >= math.ceil(int(list_with_user_data[2])/2)

#3)У всех питомцев есть имя, возраст и порода.
def test_not_empty_name_animaltype_age():
    #определяем списки имен, типов и возраста питомцев по лоkаторам
    my_pets_names = pytest.driver.find_elements(By.XPATH, '//tr/td[1]')
    my_pets_animal_types = pytest.driver.find_elements(By.XPATH, '//tr/td[2]')
    my_pets_ages = pytest.driver.find_elements(By.XPATH, '//tr/td[3]')

    #проверяем, что значения непустые
    for i in range(len(my_pets_names)):
        assert my_pets_names[i].text != ''
        assert my_pets_animal_types[i].text != ''
        assert my_pets_ages[i].text != ''


#4) У всех питомцев разные имена.
def test_all_names_are_different():
    # определяем список имен по лоkаторам

    my_pets_names = pytest.driver.find_elements(By.XPATH, '//tr/td[1]')
    #создаем пустые множества duplicates и repeated_elements
    repeated_elements = set()
    duplicates = set()
    '''проходимся по каждому элементу my_pets_names[i].text в списке my_pets_names . 
    Если элемент в множестве duplicates, мы добавляем его в множество repeated_elements. 
    Если элемент не встречается в множестве duplicates, мы добавляем его в множество duplicates. 
    В результате получаем множество repeated_elements, содержащее только повторяющиеся элементы из исходного списка.'''
    for i in range(len(my_pets_names)):
        if my_pets_names[i].text in duplicates:
            repeated_elements.add(my_pets_names[i].text)
        else:
            duplicates.add(my_pets_names[i].text)

    assert repeated_elements == set()

#5) В списке нет повторяющихся питомцев. (Сложное задание).
def test_no_double_pets():
    # определяем списки имен, типов и возраста питомцев по лоkаторам
    my_pets_names = pytest.driver.find_elements(By.XPATH, '//tr/td[1]')
    my_pets_animal_types = pytest.driver.find_elements(By.XPATH, '//tr/td[2]')
    my_pets_ages = pytest.driver.find_elements(By.XPATH, '//tr/td[3]')


    # создаем пустые множества duplicates и repeated_elements
    repeated_elements = set()
    duplicates = set()
    """Аналогично поиску питомца с повторяющейся кличкой формируем 2 множества
         с повторяющимися значениями и множеством всех питомцев
         Для сравнения формируем строку из всех 3х параметров"""
    for i in range(len(my_pets_names)):
        string_for_comparing_pets = my_pets_names[i].text + ' ' + my_pets_animal_types[i].text + ' ' + my_pets_ages[i].text
        if string_for_comparing_pets in duplicates:
            repeated_elements.add(string_for_comparing_pets)
        else:
            duplicates.add(string_for_comparing_pets)

    assert repeated_elements == set()

