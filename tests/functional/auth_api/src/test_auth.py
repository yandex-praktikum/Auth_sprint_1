import sys
sys.path.append("/tests")
import time
import logging
from functional.settings import settings

import pytest
from http import HTTPStatus

logger = logging.getLogger()

SERVICE = f"{settings.auth_api_host}:{settings.auth_api_port}"

pytestmark = pytest.mark.asyncio

USERS = [
    {
        "login": "user1",
        "email": "email1@yandex.ru",
        "name": "ruuu1",
        "password": "password1"
    },
    {
        "login": "user2",
        "email": "email2@yandex.ru",
        "name": "ruuu2",
        "password": "password2"
    },
    {
        "login": "user3",
        "email": "email3@yandex.ru",
        "name": "ruuu3",
        "password": "password3"
    },
]

async def test_signup(make_request):
    """Тестирование регистрации"""
    
    USERS[0]["login"] += str(time.time())
    
    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    logger.info(response)
    
    assert response.status in [HTTPStatus.CREATED]
    assert response.body == {}

async def test_signup_if_user_exist(make_request):
    """Тестирование повторной регистрации"""
    response = await make_request(SERVICE, "POST", "signup", USERS[0])

    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    logger.info(response)
    
    assert response.status in [HTTPStatus.CONFLICT]
    assert response.body == {}

async def test_login(make_request):
    """Тестирование входа"""
    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    logger.info(response)
    login_info = {
        "login": USERS[0]["login"],
        "password": USERS[0]["password"],
    }
    
    response = await make_request(SERVICE, "POST", "login", login_info)
    logger.info(response)
    
    assert response.status in [HTTPStatus.OK]
    assert len(response.body) == 2
    assert "access_token" in response.body
    assert "refresh_token" in response.body

async def test_login_wrong_login(make_request):
    """Тестирование входа с несуществующим логином"""
    login_info = {
        "login": "wrong_login",
        "password": USERS[0]["password"],
    }

    response = await make_request(SERVICE, "POST", "login", login_info)
    logger.info(response)

    assert response.status in [HTTPStatus.BAD_REQUEST]
    assert response.body == {}

async def test_login_wrong_login(make_request):
    """Тестирование входа с неправильным паролем"""
    login_info = {
        "login": USERS[0]["login"],
        "password": "wrong_password",
    }

    response = await make_request(SERVICE, "POST", "login", login_info)
    logger.info(response)

    assert response.status in [HTTPStatus.UNAUTHORIZED]
    assert response.body == {}

async def test_login_get(make_request):
    """Тестирование получния данных о заходах в аккаунт"""
    response = await make_request(SERVICE, "POST", "signup", USERS[1])
    login_info = {
        "login": USERS[1]["login"],
        "password": USERS[1]["password"],
    }
    response = await make_request(SERVICE, "POST", "login", login_info)
    access_token = response.body["access_token"]
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    params = {'headers': headers}
    response = await make_request(SERVICE, "GET", "login", params=params)

    assert response.status in [HTTPStatus.OK]
    assert len(response.body) != 0
    assert "user_agent" in response.body[0]
    assert "date_time" in response.body[0]

    

