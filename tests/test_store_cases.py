import pytest
from http import HTTPStatus
from api.store_api import create_order_api, get_order_api, delete_order_api
from base.base_utils import make_new_order_body, get_schema
from jsonschema import validate
from variables.config_base import STORE_STATUS_LIST
from variables.messages import ErrorMessages


@pytest.mark.parametrize("complete", [False, True])
@pytest.mark.parametrize("status", STORE_STATUS_LIST)
def test_post_orders(status, complete):
    """
    POST Тест параметризованный создания заказов
    :param
        complete: True, False
        status:  'placed', 'approved', 'delivered'
    """
    order = make_new_order_body(status, complete)
    resp = create_order_api(order)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    resp_data = resp.json()
    resp_data['shipDate'] = resp_data.get('shipDate')[:23]
    order['shipDate'] = order.get('shipDate')[:23]
    order['id'] = resp_data.get('id')
    assert resp_data == order, 'Created order is not equals received'

    order_api_schema = get_schema('order_schema.json')
    validate(resp_data, order_api_schema)

    resp = delete_order_api(resp_data.get('id'))
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value


def test_post_order_negative():
    """
    POST Тест негативный создания заказа с некорректным полем shipDate
    """
    order = make_new_order_body()
    order['shipDate'] = 'string'
    resp = create_order_api(order)
    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, \
        ErrorMessages.STATUS_CODE_NOT_EQUALS_INTERNAL_SERVER_ERROR.value


def test_get_order_by_id():
    """
    GET Тест получения заказа по ID
        1. Готовим тело Order
        2. Создаем через api новый Order
        3. Проверяем статус ответа
        4. Выполняем GET запрос по созданному ID заказа
        5. Проверяем статус ответа,
            добавляем созданный ID в подготовленное тело Order и сверяем тело запроса и ответа
        6. Валидация json схемы
        7. Удаляем созданный Order
    """
    order = make_new_order_body()
    resp = create_order_api(order)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    order_id = resp.json().get('id')
    resp = get_order_api(order_id)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    resp_data = resp.json()
    resp_data['shipDate'] = resp_data.get('shipDate')[:23]
    order['shipDate'] = order.get('shipDate')[:23]
    order['id'] = resp_data.get('id')
    assert resp_data == order, 'Created order is not equals received'

    order_api_schema = get_schema('order_schema.json')
    validate(resp_data, order_api_schema)

    resp = delete_order_api(order_id)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value


def test_get_order_negative():
    """
    GET Тест негативный получения заказа по несуществующему order_id
    """
    order_id = -1
    resp = get_order_api(order_id)
    assert resp.status_code == HTTPStatus.NOT_FOUND, ErrorMessages.STATUS_CODE_NOT_EQUALS_NOT_FOUND.value


def test_delete_order_by_id():
    """
    DELETE Тест удаления заказа по ID
        1. Готовим тело Order
        2. Создаем через api новый Order
        3. Проверяем статус ответа
        4. Выполняем DELETE запрос по созданному ID заказа
        5. Проверяем статус ответа,
            добавляем созданный ID в подготовленное тело Order и сверяем тело запроса и ответа
        6. Проверяем что в ответе в поле message - переданный order_id
    """
    order = make_new_order_body()
    resp = create_order_api(order)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    order_id = resp.json().get('id')
    resp = delete_order_api(order_id)
    assert resp.status_code == HTTPStatus.OK, ErrorMessages.STATUS_CODE_NOT_EQUALS_OK.value
    resp_data = resp.json()
    assert int(resp_data['message']) == order_id, f'Deleted order Id is not equals {order_id}'


def test_delete_order_negative():
    """
    DELETE Тест негативный удаления заказа по несуществующему order_id
    """
    order_id = -1
    resp = delete_order_api(order_id)
    assert resp.status_code == HTTPStatus.NOT_FOUND, ErrorMessages.STATUS_CODE_NOT_EQUALS_NOT_FOUND.value
