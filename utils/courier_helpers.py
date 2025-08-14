from data import urls
from data.generator import generate_courier
from utils.api_client import ApiClient
from uuid import uuid4

def register_new_courier_and_return_login_password():
    courier = generate_courier()
    courier["login"] = f"{courier['login']}_{uuid4().hex[:6]}"
    resp = ApiClient.post(urls.CREATE_COURIER, json=courier)
    if resp.status_code == 201:
        return courier["login"], courier["password"], courier["firstName"]
    return None

def login_and_get_id(login, password):
    resp = ApiClient.post(urls.LOGIN_COURIER, json={"login": login, "password": password})
    if resp.status_code == 200:
        return resp.json().get("id")
    return None

def delete_courier_by_id(courier_id):
    return ApiClient.delete(f"{urls.DELETE_COURIER}/{courier_id}")
