import requests
from variables.config_base import BASE_URL, HEADERS


def get_user_api(username):
    response = requests.get(f'{BASE_URL}/user/{username}')
    return response


def create_user_api(body):
    response = requests.post(f'{BASE_URL}/user', json=body, headers=HEADERS)
    return response


def delete_user_api(username):
    response = requests.delete(f'{BASE_URL}/user/{username}')
    return response
