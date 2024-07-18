class BaseURL:
    BASEURL = "https://qa-scooter.praktikum-services.ru"


class CourierURLs:
    create_courier = f"{BaseURL.BASEURL}/api/v1/courier"
    login_courier = f"{BaseURL.BASEURL}/api/v1/courier/login"
    delete_courier = f"{BaseURL.BASEURL}/api/v1/courier"


class OrderURLs:
    order = f"{BaseURL.BASEURL}/api/v1/orders"
    accept_order = f"{BaseURL.BASEURL}/api/v1/orders/accept"
    get_order = f"{BaseURL.BASEURL}/api/v1/orders?limit=3"
    get_order_number = f"{BaseURL.BASEURL}/api/v1/orders/track"
