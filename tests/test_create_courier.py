from unittest.mock import patch, MagicMock
import allure
import pytest
import conftest
import requests
from locators import LocatorsCourier


@allure.feature("Тест создания профиля курьера")
class TestCreateCourier:
    @allure.title("Тест успешного создания профиля курьера")
    @allure.description("Тест проверяет успешное создание профиля курьера")
    @patch('requests.post')
    @patch('conftest.register_new_courier_and_return_login_password')
    def test_create_courier_success(self, mock_register, mock_post):
        mock_register.return_value = (["login", "password", "first_name"], MagicMock(status_code=201, json=lambda: {"ok": True}))
        credentials, response = conftest.register_new_courier_and_return_login_password()
        mock_response = {
            "ok": True
        }
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_response
        assert response.status_code == 201
        assert response.json().get("ok") == True
        assert len(credentials) == 3

    @allure.title("Тест создания профиля курьера с ранее созданными логином и паролем")
    @allure.description("Тест проверяет появление ошибки про попытки создать дубликат профиля курьера")
    @patch('requests.post')
    @patch('conftest.register_new_courier_and_return_login_password')
    def test_create_duplicate_courier(self, mock_register, mock_post):
        mock_register.return_value = (
        ["login", "password", "first_name"], MagicMock(status_code=201, json=lambda: {"ok": True}))
        credentials, _ = conftest.register_new_courier_and_return_login_password()
        login, password, first_name = credentials

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        mock_response = {
            "message": "Этот логин уже используется"
        }
        mock_post.return_value.status_code = 409
        mock_post.return_value.json.return_value = mock_response
        response = requests.post(LocatorsCourier.create_courier, data=payload)
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]

    @allure.title("Тест создания профиля курьера без логина или пароля")
    @allure.description("Тест проверяет появление ошибки при попытки создать профиль курьера без логина или пароля")
    @pytest.mark.parametrize("payload, expected_status, expected_message", [
        ({"login": "", "password": "testpass", "firstName": "testname"}, 400,
         "Недостаточно данных для создания учетной записи"),
        ({"login": "testlogin", "password": "", "firstName": "testname"}, 400,
         "Недостаточно данных для создания учетной записи")
    ])
    @patch('requests.post')
    def test_create_courier_missing_credentials(self, mock_post, payload, expected_status, expected_message):
        mock_response = {
            "message": "Недостаточно данных для создания учетной записи"
        }
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = mock_response
        response = requests.post(LocatorsCourier.create_courier, json=payload)
        assert response.status_code == expected_status
        assert expected_message in response.json()["message"]
