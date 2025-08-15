import requests


class ApiClient:
    @staticmethod
    def post(url, json=None, params=None):
        return requests.post(url, json=json, params=params)

    @staticmethod
    def get(url, params=None):
        return requests.get(url, params=params)

    @staticmethod
    def put(url, params=None, json=None):
        return requests.put(url, params=params, json=json)

    @staticmethod
    def delete(url):
        return requests.delete(url)
