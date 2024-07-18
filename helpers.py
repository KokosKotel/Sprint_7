import allure
import requests
import random
import string
from data import CreateOrder
from urls import CourierURLs, OrderURLs


# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
@allure.step("Регистрируем новый профиль курьера")
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(CourierURLs.create_courier, data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass, response


@allure.step("Заходим в новый профиль курьера")
def login_courier():
    credentials, _ = register_new_courier_and_return_login_password()
    login, password, first_name = credentials
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(CourierURLs.login_courier, json=payload)
    return response


@allure.step("Регистрируем новый заказ")
def register_new_order():
    order_payload = CreateOrder.order_base
    order_response = requests.post(OrderURLs.order, json=order_payload)
    return order_response


@allure.step("Получаем id курьера")
def get_courier_id():
    credentials, _ = register_new_courier_and_return_login_password()
    login, password, first_name = credentials
    payload = {
        "login": login,
        "password": password
    }
    response_courier = requests.post(CourierURLs.login_courier, json=payload)
    courier_id = response_courier.json()["id"]
    return courier_id


@allure.step("Получаем id заказа")
def get_order_id():
    order_response = register_new_order()
    order_id = order_response.json()["track"]
    return order_id
