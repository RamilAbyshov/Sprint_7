import requests
import allure
from data import urls
from data.generator import generate_order_data
from data.test_data import GET_ORDER_NO_TRACK, GET_ORDER_INVALID_TRACK


@allure.epic("Orders API")
@allure.feature("Get order by track")
class TestGetOrderByTrack:

    @allure.title("Get order by valid track — success")
    def test_get_order_success(self):
        with allure.step("Create a new order"):
            order_resp = requests.post(urls.CREATE_ORDER, json=generate_order_data())
            track = order_resp.json()["track"]

        with allure.step("Get order using track"):
            resp = requests.get(urls.GET_ORDER_BY_TRACK, params={"t": track})
        with allure.step("Check response code and order id"):
            assert resp.status_code == 200
            assert "order" in resp.json()
            assert resp.json()["order"]["id"] > 0

    @allure.title("Get order without track — error")
    def test_get_order_no_track(self):
        with allure.step("Send GET without track"):
            resp = requests.get(urls.GET_ORDER_BY_TRACK)
        with allure.step("Check status code and error message"):
            assert resp.status_code == 400
            assert resp.json()["message"] == GET_ORDER_NO_TRACK

    @allure.title("Get order with invalid track — error")
    def test_get_order_invalid_track(self):
        with allure.step("Send GET with invalid track"):
            resp = requests.get(urls.GET_ORDER_BY_TRACK, params={"t": 99999999})
        with allure.step("Check status code and error message"):
            assert resp.status_code == 404
            assert resp.json()["message"] == GET_ORDER_INVALID_TRACK
