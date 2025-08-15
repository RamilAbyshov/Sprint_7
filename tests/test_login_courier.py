import pytest
import requests
import allure
from data import urls
from data.test_data import LOGIN_INVALID_CREDENTIALS, LOGIN_MISSING_FIELD
from utils.courier_helpers import register_new_courier_and_return_login_password, delete_courier_by_id

@allure.epic("Courier API")
@allure.feature("Login courier")
class TestLoginCourier:

    @allure.title("Courier can login successfully")
    def test_login_success(self):
        login, password, _ = register_new_courier_and_return_login_password()
        with allure.step("Send login request"):
           resp = requests.post(urls.LOGIN_COURIER, json={"login": login, "password": password})
        with allure.step("Check status code and id presence"):
            assert resp.status_code == 200
            assert "id" in resp.json()

        # cleanup
        cid = resp.json()["id"]
        if cid:
            delete_courier_by_id(cid)

    @allure.title("Login with invalid credentials — error")
    @pytest.mark.parametrize("login_in,password_in", [
        ("wrong_login", "wrong_pass"),
        ("wrong_login", "correct_pass"),
        ("correct_login", "wrong_pass")
    ])
    def test_login_invalid_credentials(self, login_in, password_in):
        real_login, real_password, _ = register_new_courier_and_return_login_password()

        login_to_use = real_login if login_in == "correct_login" else login_in
        password_to_use = real_password if password_in == "correct_pass" else password_in


        with allure.step("Send login request with invalid data"):
            resp = requests.post(urls.LOGIN_COURIER, json={"login": login_to_use, "password": password_to_use})
        with allure.step("Check status code and error message"):
            assert resp.status_code == 404
            assert resp.json()["message"] == LOGIN_INVALID_CREDENTIALS

    @allure.title("Missing required fields — error")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, missing_field):
        login, password, _ = register_new_courier_and_return_login_password()
        payload = {"login": login, "password": password}
        payload.pop(missing_field)

        with allure.step(f"Send login request without {missing_field}"):
            resp = requests.post(urls.LOGIN_COURIER, json=payload)

        with allure.step("Check status code and error message"):
            assert resp.status_code == 400
            assert resp.json()["message"] == LOGIN_MISSING_FIELD
