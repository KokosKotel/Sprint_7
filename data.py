class CreateOrder:
    order_base = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": ["BLACK"]
    }


class ExpectedMessage:
    courier_creation_duplicate = "Этот логин уже используется"
    login_failure = "Учетная запись не найдена"
    missing_data = "Недостаточно данных для создания учетной записи"
    order_acceptance_failure = "Недостаточно данных для поиска"
    order_not_found = "Заказ не найден"
    order_not_exist = "Заказа с таким id не существует"
    courier_not_exist = "Курьера с таким id не существует"
    courier_deletion_not_found = "Курьера с таким id нет"
    courier_deletion_missing_data = "Недостаточно данных для удаления курьера"
    login_missing_data = "Недостаточно данных для входа"

