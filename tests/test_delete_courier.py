import requests
import allure

from data.test_data import DELETE_COURIER_NO_ID, DELETE_COURIER_NONEXISTENT
from utils.courier_helpers import register_new_courier_and_return_login_password, login_and_get_id
from data import urls

@allure.epic("Courier API")
@allure.feature("Delete courier")
class TestDeleteCourier:

    @allure.title("Delete courier by ID — success")
    def test_delete_courier_success(self):
        login, password, _ = register_new_courier_and_return_login_password()
        cid = login_and_get_id(login, password)
        with allure.step("Delete the courier"):
            resp = requests.delete(f"{urls.DELETE_COURIER}/{cid}")
        with allure.step("Check the response"):
            assert resp.status_code == 200
            assert resp.json() == {"ok": True}

    @allure.title("Удаление курьера без ID — ошибка")
    def test_delete_courier_no_id(self):
        with allure.step("Send DELETE without id"):
            resp = requests.delete(urls.DELETE_COURIER)
        with allure.step("Check status code and error message"):
            assert resp.status_code == 400
            assert resp.json()["message"] == DELETE_COURIER_NO_ID

    @allure.title("Удаление курьера с несуществующим ID — ошибка")
    def test_delete_courier_nonexistent(self):
        with allure.step("Send DELETE with non-existent id"):
            resp = requests.delete(f"{urls.DELETE_COURIER}/99999999")
        with allure.step("Check error response"):
            assert resp.status_code == 404
            assert resp.json()["message"] == DELETE_COURIER_NONEXISTENT
