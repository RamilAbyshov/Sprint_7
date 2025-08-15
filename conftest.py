import pytest
from utils.courier_helpers import register_new_courier_and_return_login_password, login_and_get_id, delete_courier_by_id

@pytest.fixture
def new_courier():
    creds = register_new_courier_and_return_login_password()
    login, password, firstName = creds
    courier_id = login_and_get_id(login, password)
    yield {"login": login, "password": password, "firstName": firstName, "id": courier_id}
    # cleanup
    if courier_id:
        delete_courier_by_id(courier_id)
