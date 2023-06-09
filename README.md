# QAPython_API_Pytest

Реализация API тестирования https://petstore.swagger.io/

Автоматизированы три группы хэндлеров: pet, store, user
Методами GET, POST, DELETE
Позитивные и негативные тесты.

[tests](tests)
 - [test_pet_cases.py](tests%2Ftest_pet_cases.py)
 - [test_store_cases.py](tests%2Ftest_store_cases.py)
 - [test_user_cases.py](tests%2Ftest_user_cases.py)

Запуск:  
`pytest .\tests\ -v -s`