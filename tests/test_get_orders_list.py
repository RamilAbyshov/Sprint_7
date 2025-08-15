import requests
import allure
from data import urls


@allure.epic("Orders API")
@allure.feature("Getting orders")
class TestGetOrder:

    @allure.title("Get orders list")
    def test_get_orders_list(self):
        with allure.step("Send request to get list of orders"):
            resp = requests.get(urls.ORDERS_LIST)
        with allure.step("Check response format"):
            assert resp.status_code == 200
            assert "orders" in resp.json()
            assert isinstance(resp.json()["orders"], list)
