from unittest.mock import patch
import allure
import requests
import conftest
from locators import LocatorsCourier


@allure.feature("Тест удаления профиля курьера")
class TestDeleteCourier:
    @allure.title("Тест успешного удаления профиля курьера")
    @allure.description("Тест проверяет успешное удаление профиля курьера")
    @patch('requests.delete')
    def test_delete_courier_success(self, mock_delete):
        courier_id = conftest.get_courier_id()
        mock_response = {
            "ok": True
        }
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = mock_response
        response = requests.delete(f"{LocatorsCourier.delete_courier}/{courier_id}")
        assert response.status_code == 200
        assert response.json().get("ok") == True

    @allure.title("Тест удаления профиля курьера без id курьера")
    @allure.description("Тест проверяет появление ошибки при попытки удалить профиль курьера без id курьера")
    @patch('requests.delete')
    def test_delete_courier_missing_id(self, mock_delete):
        courier_id = ""
        mock_response = {
            "message": "Недостаточно данных для удаления курьера"
        }
        mock_delete.return_value.status_code = 400
        mock_delete.return_value.json.return_value = mock_response
        response = requests.delete(f"{LocatorsCourier.delete_courier}/{courier_id}")
        assert response.status_code == 400
        assert "Недостаточно данных для удаления курьера" in response.json()["message"]

    @allure.title("Тест удаления профиля курьера с несуществующим id курьера")
    @allure.description("Тест проверяет появление ошибки при попытки удалить профиль курьера с несуществующим id курьера")
    @patch('requests.delete')
    def test_delete_courier_nonexistent_id(self, mock_delete):
        courier_id = 0
        mock_response = {
            "message": "Курьера с таким id нет"
        }
        mock_delete.return_value.status_code = 404
        mock_delete.return_value.json.return_value = mock_response
        response = requests.delete(f"{LocatorsCourier.delete_courier}/{courier_id}")
        assert response.status_code == 404
        assert "Курьера с таким id нет" in response.json()["message"]
