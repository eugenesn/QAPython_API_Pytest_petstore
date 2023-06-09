import pytest
from jsonschema import validate
from http import HTTPStatus

from variables.config_base import PET_STATUS_LIST
from base.base_utils import get_schema, make_new_pet_body
from api.pets_api import get_pet_api, create_pet_api, delete_pet_api, get_pets_by_status_api
from variables.messages import ErrorMessages


def test_post_create_new_pet():
    """
    POST Тест создания нового Pet:
        1. Готовим тело Pet
        2. Создаем через api новый Pet
        3. Проверяем статус ответа,
           добавляем созданный ID в подготовленное тело Pet и сверяем тело запроса и ответа
        4. Валидация json схемы
        5. Удаляем созданный Pet
    """
    pet = make_new_pet_body()
    resp = create_pet_api(pet)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    resp_created_data = resp.json()
    pet_id = resp_created_data['id']
    pet['id'] = pet_id
    assert pet == resp_created_data, 'Created pet is not equals sent data'
    pet_schema = get_schema('pet_schema.json')
    validate(resp_created_data, pet_schema)
    resp_delete = delete_pet_api(pet_id)
    assert resp_delete.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value


def test_post_create_new_pet_negative():
    """
    POST Тест негативный добавления нового Pet:
        1. Готовим тело Pet
        2. Меняем item 'category' на некорректный
        3. Выполняем API создания нового Pet
        4. Проверяем статус ответа = INTERNAL_SERVER_ERROR
    """
    pet = make_new_pet_body()
    pet['category'] = "string"
    resp = create_pet_api(pet)
    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, \
        ErrorMessages.STATUS_CODE_NOT_EQUALS_INTERNAL_SERVER_ERROR.value


@pytest.mark.parametrize("status", PET_STATUS_LIST)
def test_get_pets_by_status(status):
    """
    GET Тест параметризованный, поиск Pets по статусам
    :param
        status:  'available', 'pending', 'sold'
    """
    resp = get_pets_by_status_api(status)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    resp_data = resp.json()
    for item in resp_data:
        assert item.get('status') == status, f'Pet status is not equals {status}'
    pets_by_status_api_schema = get_schema('pets_by_status_schema.json')
    validate(resp_data, pets_by_status_api_schema)


def test_get_pet_negative():
    """
    GET Тест негативный, поиск по несуществующему ID
    """
    pet_id = -1
    resp = get_pet_api(pet_id)
    assert resp.status_code == HTTPStatus.NOT_FOUND, ErrorMessages.STATUS_CODE_NOT_EQUALS_NOT_FOUND.value


def test_delete_pet():
    """
    DELETE Тест удаления Pet:
        1. Готовим тело Pet
        2. Создаем Pet через api новый Pet. Проверяем статус ответа
        3. Удаляем через API созданного Pet. Проверяем статус ответа и полученный в поле message - переданный Pet ID
    """
    pet = make_new_pet_body()
    resp = create_pet_api(pet)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    resp_data = resp.json()
    pet_id = resp_data['id']
    resp = delete_pet_api(pet_id)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    resp_data = resp.json()
    assert int(resp_data['message']) == pet_id, f'Deleted pet Id is not equals {pet_id}'


def test_delete_pet_negative():
    """
    DELETE Тест негативный удаления Pet по несуществующему ID
    """
    pet_id = -1
    resp = delete_pet_api(pet_id)
    assert resp.status_code == HTTPStatus.NOT_FOUND, ErrorMessages.STATUS_CODE_NOT_EQUALS_NOT_FOUND.value
