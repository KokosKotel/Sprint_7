from unittest.mock import patch
import allure
import requests
from conftest import get_order_id
from locators import LocatorsOrder


@allure.feature("Тест получение заказов по номеру")
class TestReceiveOrderNumber:
    @allure.title("Тест успешного получения заказа по номеру")
    @allure.description("Тест проверяет успешное получение заказа по его номеру")
    @patch('requests.get')
    def test_get_order_by_number_success(self, mock_get):
        order_id = get_order_id()
        mock_response = {
            "order": {
                "track": "123456"
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        response = requests.get(f"{LocatorsOrder.get_order_number}?t={order_id}")
        assert response.status_code == 200
        assert "track" in response.json()["order"]

    @allure.title("Тест получения заказа без id заказа")
    @allure.description("Тест проверяет появление ошибки при получении заказа без id заказа")
    @patch('requests.get')
    def test_get_order_by_number_missing_order_id(self, mock_get):
        order_id = ""
        mock_response = {
            "message": "Недостаточно данных для поиска"
        }
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = mock_response
        response = requests.get(f"{LocatorsOrder.get_order_number}?t={order_id}")
        assert response.status_code == 400
        assert "Недостаточно данных для поиска" in response.json()["message"]

    @allure.title("Тест получения заказа с несуществующим id заказа")
    @allure.description("Тест проверяет появление ошибки при получении заказа с несуществующим id заказа")
    @patch('requests.get')
    def test_get_order_by_number_nonexistent_order(self, mock_get):
        order_id = 0
        mock_response = {
            "message": "Заказ не найден"
        }
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = mock_response
        response = requests.get(f"{LocatorsOrder.get_order_number}?t={order_id}")
        assert response.status_code == 404
        assert "Заказ не найден" in response.json()["message"]
