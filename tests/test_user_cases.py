import string
import random
from http import HTTPStatus
from jsonschema import validate

from api.users_api import create_user_api, get_user_api, delete_user_api
from base.base_utils import get_schema, make_new_user_body
from variables.messages import ErrorMessages


def test_post_create_user():
    """
    POST Тест создания нового User:
        1. Готовим тело User
        2. Создаем через api новый User
        3. Проверяем статус ответа и запоминаем созданный ID из поля message
        4. Добавляем созданный ID в подготовленное тело User
        5. Получаем созданный User по username
        6. Сверяем подготовленный User с полученным в ответе
        7. Удаляем созданный User
    """
    user = make_new_user_body()
    resp = create_user_api(user)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    resp_created_data = resp.json()
    user_id = int(resp_created_data['message'])
    user['id'] = user_id
    username = user.get("username")
    resp = get_user_api(username)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    resp_data = resp.json()
    assert user == resp_data, 'Created user is not equals sent data'
    resp = delete_user_api(username)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value


def test_post_create_user_negative():
    """
    POST Тест негативный создания User с некорректным полем userStatus
    """
    user = make_new_user_body()
    user['userStatus'] = 'string'
    resp = create_user_api(user)
    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value


def test_get_user():
    """
    GET Тест получения User по username
        1. Готовим тело User
        2. Создаем через api новый User
        3. Проверяем статус ответа
        4. Выполняем GET запрос по созданному username User
        5. Проверяем статус ответа,
            добавляем созданный ID в подготовленное тело User и сверяем тело запроса и ответа
        6. Валидация json схемы
        7. Удаляем созданный User
    """
    user = make_new_user_body()
    resp = create_user_api(user)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    username = user.get("username")
    resp = get_user_api(username)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    resp_data = resp.json()
    user_id = resp_data['id']
    user['id'] = user_id
    assert user == resp_data, 'Default user body is not equals requested data'

    user_api_schema = get_schema('user_schema.json')
    validate(resp_data, user_api_schema)

    resp = delete_user_api(username)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value


def test_get_user_negative():
    """
    GET Тест негативный получения User по несуществующему username
    """
    user = make_new_user_body()
    username_fake = user.get("username").join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
    resp = get_user_api(username_fake)
    assert resp.status_code == HTTPStatus.NOT_FOUND, ErrorMessages.STATUS_CODE_NOT_EQUALS_NOT_FOUND.value


def test_delete_user():
    """
    DELETE Тест удаления User по username
        1. Готовим тело User
        2. Создаем через api новый User
        3. Проверяем статус ответа
        4. Выполняем DELETE запрос по созданному username User
        5. Проверяем статус ответа
        6. Выполняем запрос на получение удаленного User по username
        7. Проверяем статус ответа
    """
    user = make_new_user_body()
    resp = create_user_api(user)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    username = user.get("username")
    resp = delete_user_api(username)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    resp = get_user_api(username)
    assert resp.status_code == HTTPStatus.NOT_FOUND, ErrorMessages.STATUS_CODE_NOT_EQUALS_NOT_FOUND.value


def test_delete_user_negative():
    """
    DELETE Тест удаления User негативный по username
        1. Готовим тело User
        2. Создаем через api новый User
        3. Проверяем статус ответа
        4. Выполняем DELETE запрос по не-существующему username_fake User
        5. Проверяем статус ответа
        6. Удаляем созданный User по username
        7. Проверяем статус ответа
    """
    user = make_new_user_body()
    resp = create_user_api(user)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    username = user.get("username")
    username_fake = user.get("username").join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
    resp = delete_user_api(username_fake)
    assert resp.status_code == HTTPStatus.NOT_FOUND, ErrorMessages.STATUS_CODE_NOT_EQUALS_NOT_FOUND.value
    resp = delete_user_api(username)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
