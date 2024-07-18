import allure
import pytest
import requests

from data import ExpectedMessage
from helpers import login_courier, register_new_courier_and_return_login_password
from urls import CourierURLs


@allure.feature("Тест входа в профиль курьера")
class TestLoginCourier:
    @allure.title("Тест успешного входа в профиль курьера")
    @allure.description("Тест проверяет Успешный вход в профиль курьера")
    def test_login_courier_success(self):
        response = login_courier()
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Тест входа в профиль курьера с неверным логином или паролем")
    @allure.description("Тест проверяет появление ошибки в профиль курьера с неверным логином(1) и паролем(2)")
    @pytest.mark.parametrize("login, password, expected_status", [
        ("invalidlogin", "valid_password", 404),
        ("valid_login", "invalidpass", 404)
    ])
    def test_login_invalid_credentials(self, login, password, expected_status, ):
        credentials, _ = register_new_courier_and_return_login_password()
        valid_login, valid_password, first_name = credentials
        payload = {
            "login": login if login != "valid_login" else valid_login,
            "password": password if password != "valid_password" else valid_password
        }
        response = requests.post(CourierURLs.login_courier, json=payload)
        assert response.status_code == expected_status
        assert ExpectedMessage.login_failure in response.json()["message"]

    @allure.title("Тест входа в профиль курьера без логина или пароля")
    @allure.description("Тест проверяет появление ошибки при попытки входа в профиль курьера без логина(1) и пароля(2)")
    @pytest.mark.parametrize("login, password, expected_status", [
        ("", "valid_password", 400),
        ("valid_login", "", 400)
    ])
    def test_login_missing_credentials(self, login, password, expected_status):
        credentials, _ = register_new_courier_and_return_login_password()
        valid_login, valid_password, first_name = credentials
        payload = {
            "login": login if login is "" else valid_login,
            "password": password if password is "" else valid_password
        }
        response = requests.post(CourierURLs.login_courier, json=payload)
        assert response.status_code == 400
        assert ExpectedMessage.login_missing_data in response.json()["message"]

    @allure.title("Тест входа в профиль курьера с несуществующим логином и паролем")
    @allure.description("Тест проверяет появление ошибки при попытки входа в профиль курьера с несуществующим логином и паролем")
    def test_login_nonexistent_user(self):
        payload = {
            "login": "nonlogin",
            "password": "nonpass"
        }
        response = requests.post(CourierURLs.login_courier, json=payload)
        assert response.status_code == 404
        assert ExpectedMessage.login_failure in response.json()["message"]
