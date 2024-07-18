import allure
import pytest
import requests
from urls import OrderURLs


@allure.feature("Тест заказов")
class TestOrders:
    @allure.title("Тест успешных заказов с разными цветами")
    @allure.description("Тест проверяет, что заказ успешно принят при разных цветах самоката")
    @pytest.mark.parametrize("colors, expected_status", [
        (["BLACK"], 201),
        (["GREY"], 201),
        (["BLACK", "GREY"], 201),
        ([], 201)
    ])
    def test_create_order_color(self, colors, expected_status):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": colors
        }
        response = requests.post(OrderURLs.order, json=payload)
        assert response.status_code == expected_status
        assert "track" in response.json()

    @allure.title("Тест получения списка заказа")
    @allure.description("Тест проверяет успешное получение списка заказов")
    def test_list_order(self):
        response = requests.get(OrderURLs.get_order)
        assert response.status_code == 200
        assert isinstance(response.json().get("orders"), list)
        assert len(response.json().get("orders")) > 0
