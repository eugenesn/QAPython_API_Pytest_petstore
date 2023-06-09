import requests
from variables.config_base import BASE_URL, HEADERS


def get_order_api(order_id):
    response = requests.get(f'{BASE_URL}/store/order/{order_id}')
    return response


def create_order_api(body):
    response = requests.post(f'{BASE_URL}/store/order', json=body, headers=HEADERS)
    return response


def delete_order_api(store_id):
    response = requests.delete(f'{BASE_URL}/store/order/{store_id}')
    return response
