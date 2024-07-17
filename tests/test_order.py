from unittest.mock import patch
import allure
import pytest
import requests
from locators import LocatorsOrder


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
    @patch("requests.post")
    def test_create_order_color(self, mock_post, colors, expected_status):
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
        mock_response = {
            "track": "123456"
        }
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_response
        response = requests.post(LocatorsOrder.order, json=payload)
        assert response.status_code == expected_status
        assert "track" in response.json()

    @allure.title("Тест получения списка заказа")
    @allure.description("Тест проверяет успешное получение списка заказов")
    @patch("requests.get")
    def test_list_order(self, mock_get):
        mock_response = {
            "orders": [{"id": 12}, {"id": 123}]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        response = requests.get(LocatorsOrder.get_order)
        assert response.status_code == 200
        assert isinstance(response.json().get("orders"), list)
        assert len(response.json().get("orders")) > 0
