import pytest
import requests
import allure
from data import urls, test_data
from data.generator import generate_order_data


@allure.epic("Orders API")
@allure.feature("Order Creation")
class TestCreateOrder:

    @pytest.mark.parametrize("colors", [
        test_data.COLORS_BLACK,
        test_data.COLORS_GREY,
        test_data.COLORS_BOTH,
        test_data.COLORS_NONE
    ])
    @allure.title("Create order with different color options")
    def test_create_order_with_colors(self, colors):
        with allure.step("Generate order data"):
            order_data = generate_order_data(colors)
        with allure.step("Send request to create order"):
            resp = requests.post(urls.CREATE_ORDER, json=order_data)
        with allure.step("Check response code and track presence"):
            assert resp.status_code == 201
            assert "track" in resp.json()
