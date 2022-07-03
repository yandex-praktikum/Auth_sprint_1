import sys

sys.path.append("/tests")
import logging
import os
import time
from http import HTTPStatus

import pytest
from dotenv import load_dotenv
from functional.settings import settings

load_dotenv()

SERVICE = f"{settings.auth_api_host}:{settings.auth_api_port}"

pytestmark = pytest.mark.asyncio

USERS = [
    {
        "login": "user1",
        "email": "email1@yandex.ru",
        "name": "ruuu1",
        "password": "password1",
    },
    {
        "login": "user2",
        "email": "email2@yandex.ru",
        "name": "ruuu2",
        "password": "password2",
    },
    {
        "login": "user3",
        "email": "email3@yandex.ru",
        "name": "ruuu3",
        "password": "password3",
    },
]


async def test_signup(make_request):
    """Тестирование регистрации"""

    USERS[0]["login"] += str(time.time())

    response = await make_request(SERVICE, "POST", "signup", USERS[0])

    assert response.status in [HTTPStatus.CREATED]
    assert response.body == {}


async def test_signup_if_user_exist(make_request):
    """Тестирование повторной регистрации"""
    response = await make_request(SERVICE, "POST", "signup", USERS[0])

    response = await make_request(SERVICE, "POST", "signup", USERS[0])

    assert response.status in [HTTPStatus.CONFLICT]
    assert response.body == {}


async def test_login(make_request):
    """Тестирование входа"""
    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    login_info = {
        "login": USERS[0]["login"],
        "password": USERS[0]["password"],
    }

    response = await make_request(SERVICE, "POST", "login", login_info)

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

    assert response.status in [HTTPStatus.BAD_REQUEST]
    assert response.body == {}


async def test_login_wrong_login(make_request):
    """Тестирование входа с неправильным паролем"""
    login_info = {
        "login": USERS[0]["login"],
        "password": "wrong_password",
    }

    response = await make_request(SERVICE, "POST", "login", login_info)

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
    headers = {"Authorization": "Bearer " + access_token}

    response = await make_request(SERVICE, "GET", "login", headers=headers)

    assert response.status in [HTTPStatus.OK]
    assert len(response.body) != 0
    assert "user_agent" in response.body[0]
    assert "date_time" in response.body[0]


async def test_login_get_wrong(make_request):
    """Тестирование получния данных о заходах в аккаунт для неправильного токена"""
    headers = {"Authorization": "Bearer " + "wrong_tocken"}

    response = await make_request(SERVICE, "GET", "login", headers=headers)

    assert response.status in [HTTPStatus.UNPROCESSABLE_ENTITY]


async def test_refresh_token(make_request):
    """Проверка обновления токенов"""
    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    login_info = {
        "login": USERS[0]["login"],
        "password": USERS[0]["password"],
    }
    response = await make_request(SERVICE, "POST", "login", login_info)
    refresh_token = response.body["refresh_token"]
    headers = {"Authorization": "Bearer " + refresh_token}

    response = await make_request(SERVICE, "POST", "refresh", headers=headers)

    assert response.status in [HTTPStatus.OK]
    assert len(response.body) == 2
    assert "access_token" in response.body
    assert "refresh_token" in response.body


async def test_refresh_token_duble(make_request):
    """Проверка обновления токенов при повторе одного токена"""
    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    login_info = {
        "login": USERS[0]["login"],
        "password": USERS[0]["password"],
    }
    response = await make_request(SERVICE, "POST", "login", login_info)
    refresh_token = response.body["refresh_token"]
    headers = {"Authorization": "Bearer " + refresh_token}
    response = await make_request(SERVICE, "POST", "refresh", headers=headers)

    response = await make_request(SERVICE, "POST", "refresh", headers=headers)

    assert response.status in [HTTPStatus.UNAUTHORIZED]
    assert response.body == {}


async def test_logout(make_request):
    """Проверка выхода из акаутна"""
    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    login_info = {
        "login": USERS[0]["login"],
        "password": USERS[0]["password"],
    }
    response = await make_request(SERVICE, "POST", "login", login_info)
    access_token = response.body["access_token"]
    headers = {"Authorization": "Bearer " + access_token}

    response = await make_request(SERVICE, "DELETE", "logout", headers=headers)

    assert response.status in [HTTPStatus.OK]
    assert response.body == {}


async def test_logout_refresh(make_request):
    """Проверка работоспособности refresh токена при выходе из акаунта"""
    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    login_info = {
        "login": USERS[0]["login"],
        "password": USERS[0]["password"],
    }
    response = await make_request(SERVICE, "POST", "login", login_info)
    access_token = response.body["access_token"]
    refresh_token = response.body["refresh_token"]
    headers = {"Authorization": "Bearer " + access_token}
    response = await make_request(SERVICE, "DELETE", "logout", headers=headers)
    headers = {"Authorization": "Bearer " + refresh_token}

    response = await make_request(SERVICE, "POST", "refresh", headers=headers)

    assert response.status in [HTTPStatus.UNAUTHORIZED]
    assert response.body == {}


async def test_logout_login_info(make_request):
    """Проверка работоспособности access токена при выходе из акаунта"""
    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    login_info = {
        "login": USERS[0]["login"],
        "password": USERS[0]["password"],
    }
    response = await make_request(SERVICE, "POST", "login", login_info)
    access_token = response.body["access_token"]
    headers = {"Authorization": "Bearer " + access_token}
    response = await make_request(SERVICE, "DELETE", "logout", headers=headers)

    response = await make_request(SERVICE, "GET", "login", headers=headers)

    assert response.status in [HTTPStatus.UNAUTHORIZED]


async def test_admin_user(make_request):

    ADMIN_USER = {
        "login": os.environ.get("ADMIN_LOGIN"),
        "password": os.environ.get("ADMIN_PASSWORD"),
    }

    response = await make_request(SERVICE, "POST", "login", ADMIN_USER)
    access_token = response.body["access_token"]
    headers = {"Authorization": "Bearer " + access_token}

    response = await make_request(SERVICE, "GET", "login", headers=headers)

    assert response.status in [HTTPStatus.OK]
    assert len(response.body) != 0
    assert "user_agent" in response.body[0]
    assert "date_time" in response.body[0]
