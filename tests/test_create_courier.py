import allure
import pytest
import requests

from data import ExpectedMessage
from helpers import register_new_courier_and_return_login_password
from urls import CourierURLs


@allure.feature("Тест создания профиля курьера")
class TestCreateCourier:
    @allure.title("Тест успешного создания профиля курьера")
    @allure.description("Тест проверяет успешное создание профиля курьера")
    def test_create_courier_success(self):
        credentials, response = register_new_courier_and_return_login_password()
        assert response.status_code == 201
        assert response.json().get("ok") == True
        assert len(credentials) == 3

    @allure.title("Тест создания профиля курьера с ранее созданными логином и паролем")
    @allure.description("Тест проверяет появление ошибки про попытки создать дубликат профиля курьера")
    def test_create_duplicate_courier(self):
        credentials, _ = register_new_courier_and_return_login_password()
        login, password, first_name = credentials

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(CourierURLs.create_courier, data=payload)
        assert response.status_code == 409
        assert ExpectedMessage.courier_creation_duplicate in response.json()["message"]

    @allure.title("Тест создания профиля курьера без логина или пароля")
    @allure.description("Тест проверяет появление ошибки при попытки создать профиль курьера без логина или пароля")
    @pytest.mark.parametrize("payload, expected_status", [
        ({"login": "", "password": "testpass", "firstName": "testname"}, 400),
        ({"login": "testlogin", "password": "", "firstName": "testname"}, 400)
    ])
    def test_create_courier_missing_credentials(self, payload, expected_status):
        response = requests.post(CourierURLs.create_courier, json=payload)
        assert response.status_code == expected_status
        assert ExpectedMessage.missing_data in response.json()["message"]
