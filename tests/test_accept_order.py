import requests
import allure
from data import urls
from data.generator import generate_order_data
from utils.courier_helpers import register_new_courier_and_return_login_password, login_and_get_id

@allure.epic("Orders API")
@allure.feature("Accept order")
class TestAcceptOrder:

    @allure.title("Order acceptance by courier — success")
    def test_accept_order_success(self):
        with allure.step("Register new courier and get credentials"):
            login, password, _ = register_new_courier_and_return_login_password()
            courier_id = login_and_get_id(login, password)

        with allure.step("Create a new order"):
            order_resp = requests.post(urls.CREATE_ORDER, json=generate_order_data())
            track = order_resp.json()["track"]

        with allure.step("Get order ID by track"):
            order_resp_by_track = requests.get(urls.GET_ORDER_BY_TRACK, params={"t": track})
            order_id = order_resp_by_track.json()["order"]["id"]

        with allure.step("Accept the order with courier ID"):
            resp = requests.put(f"{urls.ACCEPT_ORDER}/{order_id}", params={"courierId": courier_id})

        with allure.step("Verify successful acceptance"):
            assert resp.status_code == 200
            assert resp.json().get("ok") is True

    @allure.title("Order acceptance without courierId — error")
    def test_accept_order_no_courier_id(self):
        with allure.step("Create a new order"):
            order_resp = requests.post(urls.CREATE_ORDER, json=generate_order_data())
            track = order_resp.json()["track"]

        with allure.step("Get order ID by track"):
            order_id = requests.get(urls.GET_ORDER_BY_TRACK, params={"t": track}).json()["order"]["id"]

        with allure.step("Try accepting the order without courierId"):
            resp = requests.put(f"{urls.ACCEPT_ORDER}/{order_id}")

        with allure.step("Verify error response"):
            assert resp.status_code == 400
            assert resp.json()["message"] == "Недостаточно данных для поиска"

    @allure.title("Order acceptance with invalid courierId — error")
    def test_accept_order_invalid_courier_id(self):
        with allure.step("Create a new order"):
            order_resp = requests.post(urls.CREATE_ORDER, json=generate_order_data())
            track = order_resp.json()["track"]

        with allure.step("Get order ID by track"):
            order_id = requests.get(urls.GET_ORDER_BY_TRACK, params={"t": track}).json()["order"]["id"]

        with allure.step("Try accepting the order with invalid courierId"):
            resp = requests.put(f"{urls.ACCEPT_ORDER}/{order_id}", params={"courierId": 99999999})

        with allure.step("Verify error response"):
            assert resp.status_code == 404
            assert resp.json()["message"] == "Курьера с таким id не существует"

    @allure.title("Order acceptance with invalid orderId — error")
    def test_accept_order_invalid_order_id(self):
        with allure.step("Register new courier and get credentials"):
            login, password, _ = register_new_courier_and_return_login_password()
            courier_id = login_and_get_id(login, password)

        with allure.step("Try accepting an order with invalid orderId"):
            resp = requests.put(f"{urls.ACCEPT_ORDER}/99999999", params={"courierId": courier_id})

        with allure.step("Verify error response"):
            assert resp.status_code == 404
            assert resp.json()["message"] == "Заказа с таким id не существует"
