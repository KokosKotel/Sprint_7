import sys
import os
import allure
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data import ExpectedMessage
from helpers import get_order_id, get_courier_id
from urls import OrderURLs


@allure.feature("Тест принятых заказов")
class TestAcceptOrder:
    @allure.title("Тест успешно принятого заказа курьером")
    @allure.description("Тест проверяет успешное принятие заказа курьером")
    def test_accept_order_success(self):
        courier_id = get_courier_id()
        order_id = get_order_id()
        response = requests.put(f"{OrderURLs.accept_order}/1?courierId={courier_id}&orderId={order_id}")
        assert response.status_code == 200
        assert response.json().get("ok") == True

    @allure.title("Тест получения заказа курьером без id курьера")
    @allure.description("Тест проверяет появление ошибки при получении заказа курьером без id курьера")
    def test_accept_order_missing_courier_id(self):
        order_id = get_order_id()
        courier_id = ""
        response = requests.put(f"{OrderURLs.accept_order}/1?courierId={courier_id}&orderId={order_id}")
        assert response.status_code == 400
        assert ExpectedMessage.order_acceptance_failure in response.json()["message"]

    @allure.title("Тест получения заказа курьером без id заказа")
    @allure.description("Тест проверяет появление ошибки при получении заказа курьером без id заказа")
    def test_accept_order_missing_order_id(self):
        courier_id = get_courier_id()
        order_id = ""
        response = requests.put(f"{OrderURLs.accept_order}/1?courierId={courier_id}&orderId={order_id}")
        assert response.status_code == 400
        assert ExpectedMessage.order_acceptance_failure in response.json()["message"]

    @allure.title("Тест получения заказа курьером с несуществующим id курьера")
    @allure.description("Тест проверяет появление ошибки при получении заказа курьером с несуществующим id курьера")
    def test_accept_order_invalid_courier_id(self):
        order_id = get_order_id()
        courier_id = 0
        response = requests.put(f"{OrderURLs.accept_order}/1?courierId={courier_id}&orderId={order_id}")
        assert response.status_code == 404
        assert ExpectedMessage.courier_not_exist in response.json()["message"]

    @allure.title("Тест получения заказа курьером с несуществующим id заказа")
    @allure.description("Тест проверяет появление ошибки при получении заказа курьером с несуществующим id заказа")
    def test_accept_order_invalid_order_id(self):
        courier_id = get_courier_id()
        order_id = 0
        response = requests.put(f"{OrderURLs.accept_order}/1?courierId={courier_id}&orderId={order_id}")
        assert response.status_code == 404
        assert ExpectedMessage.order_not_exist in response.json()["message"]
