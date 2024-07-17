from unittest.mock import patch
import allure
import requests
import conftest
from locators import LocatorsOrder


@allure.feature("Тест принятых заказов")
class TestAcceptOrder:
    @allure.title("Тест успешно принятого заказа курьером")
    @allure.description("Тест проверяет успешное принятие заказа курьером")
    @patch('requests.put')
    def test_accept_order_success(self, mock_put):
        courier_id = conftest.get_courier_id()
        order_id = conftest.get_order_id()
        mock_response = {
            "ok": True
        }
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = mock_response
        response = requests.put(f"{LocatorsOrder.accept_order}/1?courierId={courier_id}&orderId={order_id}")
        assert response.status_code == 200
        assert response.json().get("ok") == True

    @allure.title("Тест получения заказа курьером без id курьера")
    @allure.description("Тест проверяет появление ошибки при получении заказа курьером без id курьера")
    @patch('requests.put')
    def test_accept_order_missing_courier_id(self, mock_put):
        order_id = conftest.get_order_id()
        courier_id = ""
        mock_response = {
            "message": "Недостаточно данных для поиска"
        }
        mock_put.return_value.status_code = 400
        mock_put.return_value.json.return_value = mock_response
        response = requests.put(f"{LocatorsOrder.accept_order}/1?courierId={courier_id}&orderId={order_id}")
        assert response.status_code == 400
        assert "Недостаточно данных для поиска" in response.json()["message"]

    @allure.title("Тест получения заказа курьером без id заказа")
    @allure.description("Тест проверяет появление ошибки при получении заказа курьером без id заказа")
    @patch('requests.put')
    def test_accept_order_missing_order_id(self, mock_put):
        courier_id = conftest.get_courier_id()
        order_id = ""
        mock_response = {
            "message": "Недостаточно данных для поиска"
        }
        mock_put.return_value.status_code = 400
        mock_put.return_value.json.return_value = mock_response
        response = requests.put(f"{LocatorsOrder.accept_order}/1?courierId={courier_id}&orderId={order_id}")
        assert response.status_code == 400
        assert "Недостаточно данных для поиска" in response.json()["message"]

    @allure.title("Тест получения заказа курьером с несуществующим id курьера")
    @allure.description("Тест проверяет появление ошибки при получении заказа курьером с несуществующим id курьера")
    @patch('requests.put')
    def test_accept_order_invalid_courier_id(self, mock_put):
        order_id = conftest.get_order_id()
        courier_id = 0
        mock_response = {
            "message": "Курьера с таким id не существует"
        }
        mock_put.return_value.status_code = 404
        mock_put.return_value.json.return_value = mock_response
        response = requests.put(f"{LocatorsOrder.accept_order}/1?courierId={courier_id}&orderId={order_id}")
        assert response.status_code == 404
        assert "Курьера с таким id не существует" in response.json()["message"]

    @allure.title("Тест получения заказа курьером с несуществующим id заказа")
    @allure.description("Тест проверяет появление ошибки при получении заказа курьером с несуществующим id заказа")
    @patch('requests.put')
    def test_accept_order_invalid_order_id(self, mock_put):
        courier_id = conftest.get_courier_id()
        order_id = 0
        mock_response = {
            "message": "Заказа с таким id не существует"
        }
        mock_put.return_value.status_code = 404
        mock_put.return_value.json.return_value = mock_response
        response = requests.put(f"{LocatorsOrder.accept_order}/1?courierId={courier_id}&orderId={order_id}")
        assert response.status_code == 404
        assert "Заказа с таким id не существует" in response.json()["message"]
