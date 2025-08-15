import pytest
import requests
import allure
from data import urls
from data.generator import generate_courier
from data.test_data import CREATE_COURIER_DUPLICATE, CREATE_COURIER_MISSING_FIELD
from utils.courier_helpers import register_new_courier_and_return_login_password, login_and_get_id, delete_courier_by_id

@allure.epic("Courier API")
@allure.feature("Create courier")
class TestCreateCourier:

    @allure.title("Create a courier successfully")
    def test_create_courier_success(self):
        courier = generate_courier()
        with allure.step("Send request to create courier"):
            resp = requests.post(urls.CREATE_COURIER, json=courier)
        with allure.step("Check status code and response body"):
            assert resp.status_code == 201
            assert resp.json() == {"ok": True}

        # cleanup
        with allure.step("Cleanup: delete created courier"):
            cid = login_and_get_id(courier["login"], courier["password"])
            if cid:
                delete_courier_by_id(cid)

    @allure.title("Cannot create duplicate courier")
    def test_create_courier_duplicate(self):
        login, password, firstName = register_new_courier_and_return_login_password()
        with allure.step("Try to create courier with same login"):
            resp = requests.post(urls.CREATE_COURIER, json={"login": login, "password": password, "firstName": firstName})
        with allure.step("Check status code and message"):
            assert resp.status_code == 409
            assert resp.json()["message"] == CREATE_COURIER_DUPLICATE

    @allure.title("Missing required fields prevents courier creation")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        with allure.step("Generate courier data"):
            courier = generate_courier()
            courier.pop(missing_field)
        with allure.step(f"Send request without {missing_field}"):
            resp = requests.post(urls.CREATE_COURIER, json=courier)
        with allure.step("Check status code and error message"):
            assert resp.status_code == 400
            assert resp.json()["message"] == CREATE_COURIER_MISSING_FIELD
