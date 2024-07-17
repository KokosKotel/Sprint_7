import requests
import random
import string
from locators import LocatorsCourier, LocatorsOrder


# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
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
    response = requests.post(LocatorsCourier.create_courier, data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass, response


def login_courier():
    credentials, _ = register_new_courier_and_return_login_password()
    login, password, first_name = credentials
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(LocatorsCourier.login_courier, json=payload)
    return response


def register_new_order():
    order_payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": ["BLACK"]
    }
    order_response = requests.post(LocatorsOrder.order, json=order_payload)
    return order_response


def get_courier_id():
    credentials, _ = register_new_courier_and_return_login_password()
    login, password, first_name = credentials
    payload = {
        "login": login,
        "password": password
    }
    response_courier = requests.post(LocatorsCourier.login_courier, json=payload)
    courier_id = response_courier.json()["id"]
    return courier_id


def get_order_id():
    order_response = register_new_order()
    order_id = order_response.json()["track"]
    return order_id
