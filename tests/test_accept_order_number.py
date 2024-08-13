import allure
import requests

from data import ExpectedMessage
from helpers import get_order_id
from urls import OrderURLs


@allure.feature("Тест получение заказов по номеру")
class TestReceiveOrderNumber:
    @allure.title("Тест успешного получения заказа по номеру")
    @allure.description("Тест проверяет успешное получение заказа по его номеру")
    def test_get_order_by_number_success(self):
        order_id = get_order_id()
        response = requests.get(f"{OrderURLs.get_order_number}?t={order_id}")
        assert response.status_code == 200
        assert "track" in response.json()["order"]

    @allure.title("Тест получения заказа без id заказа")
    @allure.description("Тест проверяет появление ошибки при получении заказа без id заказа")
    def test_get_order_by_number_missing_order_id(self):
        order_id = ""
        response = requests.get(f"{OrderURLs.get_order_number}?t={order_id}")
        assert response.status_code == 400
        assert ExpectedMessage.order_acceptance_failure in response.json()["message"]

    @allure.title("Тест получения заказа с несуществующим id заказа")
    @allure.description("Тест проверяет появление ошибки при получении заказа с несуществующим id заказа")
    def test_get_order_by_number_nonexistent_order(self):
        order_id = 0
        response = requests.get(f"{OrderURLs.get_order_number}?t={order_id}")
        assert response.status_code == 404
        assert ExpectedMessage.order_not_found in response.json()["message"]
