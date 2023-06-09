import requests
from variables.config_base import BASE_URL, HEADERS


def get_pet_api(pet_id):
    response = requests.get(f'{BASE_URL}/pet/{pet_id}')
    return response


def create_pet_api(body):
    response = requests.post(f'{BASE_URL}/pet', json=body, headers=HEADERS)
    return response


def delete_pet_api(pet_id):
    response = requests.delete(f'{BASE_URL}/pet/{pet_id}')
    return response


def get_pets_by_status_api(status):
    payload = {'status': status}
    return requests.get(f'{BASE_URL}/pet/findByStatus', params=payload)
