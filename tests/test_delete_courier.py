import allure
import requests

from data import ExpectedMessage
from helpers import get_courier_id
from urls import CourierURLs


@allure.feature("Тест удаления профиля курьера")
class TestDeleteCourier:
    @allure.title("Тест успешного удаления профиля курьера")
    @allure.description("Тест проверяет успешное удаление профиля курьера")
    def test_delete_courier_success(self):
        courier_id = get_courier_id()
        response = requests.delete(f"{CourierURLs.delete_courier}/{courier_id}")
        assert response.status_code == 200
        assert response.json().get("ok") == True

    @allure.title("Тест удаления профиля курьера без id курьера")
    @allure.description("Тест проверяет появление ошибки при попытки удалить профиль курьера без id курьера")
    def test_delete_courier_missing_id(self):
        courier_id = ""
        response = requests.delete(f"{CourierURLs.delete_courier}/{courier_id}")
        assert response.status_code == 400
        assert ExpectedMessage.courier_deletion_missing_data in response.json()["message"]

    @allure.title("Тест удаления профиля курьера с несуществующим id курьера")
    @allure.description("Тест проверяет появление ошибки при попытки удалить профиль курьера с несуществующим id курьера")
    def test_delete_courier_nonexistent_id(self):
        courier_id = 0
        response = requests.delete(f"{CourierURLs.delete_courier}/{courier_id}")
        assert response.status_code == 404
        assert ExpectedMessage.courier_deletion_not_found in response.json()["message"]
