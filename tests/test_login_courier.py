from unittest.mock import patch, MagicMock
import allure
import pytest
import requests
import conftest
from locators import LocatorsCourier


@allure.feature("Тест входа в профиль курьера")
class TestLoginCourier:
    @allure.title("Тест успешного входа в профиль курьера")
    @allure.description("Тест проверяет Успешный вход в профиль курьера")
    @patch('requests.post')
    @patch('conftest.register_new_courier_and_return_login_password')
    def test_login_courier_success(self, mock_register, mock_post):
        mock_register.return_value = (["login", "password", "first_name"], MagicMock(status_code=201, json=lambda: {"ok": True}))
        mock_response = {
            "id": 123
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response
        response = conftest.login_courier()
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Тест входа в профиль курьера с неверным логином или паролем")
    @allure.description("Тест проверяет появление ошибки в профиль курьера с неверным логином(1) и паролем(2)")
    @pytest.mark.parametrize("login, password, expected_status, expected_message", [
        ("invalidlogin", "valid_password", 404, "Учетная запись не найдена"),
        ("valid_login", "invalidpass", 404, "Учетная запись не найдена")
    ])
    @patch('requests.post')
    @patch('conftest.register_new_courier_and_return_login_password')
    def test_login_invalid_credentials(self, mock_register, mock_post, login, password, expected_status, expected_message):
        mock_register.return_value = (["login", "password", "first_name"], MagicMock(status_code=201, json=lambda: {"ok": True}))
        credentials, _ = conftest.register_new_courier_and_return_login_password()
        valid_login, valid_password, first_name = credentials
        payload = {
            "login": login if login != "valid_login" else valid_login,
            "password": password if password != "valid_password" else valid_password
        }
        mock_response = {
            "message": "Учетная запись не найдена"
        }
        mock_post.return_value.status_code = 404
        mock_post.return_value.json.return_value = mock_response
        response = requests.post(LocatorsCourier.login_courier, json=payload)
        assert response.status_code == expected_status
        assert expected_message in response.json()["message"]

    @allure.title("Тест входа в профиль курьера без логина или пароля")
    @allure.description("Тест проверяет появление ошибки при попытки входа в профиль курьера без логина(1) и пароля(2)")
    @pytest.mark.parametrize("login, password, expected_status, expected_message", [
        ("", "valid_password", 400, "Недостаточно данных для входа"),
        ("valid_login", "", 400, "Недостаточно данных для входа")
    ])
    @patch('requests.post')
    @patch('conftest.register_new_courier_and_return_login_password')
    def test_login_missing_credentials(self, mock_register, mock_post, login, password, expected_status, expected_message):
        mock_register.return_value = (["login", "password", "first_name"], MagicMock(status_code=201, json=lambda: {"ok": True}))
        credentials, _ = conftest.register_new_courier_and_return_login_password()
        valid_login, valid_password, first_name = credentials
        payload = {
            "login": login if login is "" else valid_login,
            "password": password if password is "" else valid_password
        }
        mock_response = {
            "message": "Недостаточно данных для входа"
        }
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = mock_response
        response = requests.post(LocatorsCourier.login_courier, json=payload)
        assert response.status_code == 400
        assert expected_message in response.json()["message"]

    @allure.title("Тест входа в профиль курьера с несуществующим логином и паролем")
    @allure.description("Тест проверяет появление ошибки при попытки входа в профиль курьера с несуществующим логином и паролем")
    @patch('requests.post')
    def test_login_nonexistent_user(self, mock_post):
        payload = {
            "login": "nonlogin",
            "password": "nonpass"
        }
        mock_response = {
            "message": "Учетная запись не найдена"
        }
        mock_post.return_value.status_code = 404
        mock_post.return_value.json.return_value = mock_response
        response = requests.post(LocatorsCourier.login_courier, json=payload)
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]
