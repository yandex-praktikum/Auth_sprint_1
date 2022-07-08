import sys

sys.path.append("/tests")
import logging
import os
import time

from dotenv import load_dotenv
from functional.settings import settings

load_dotenv()

from http import HTTPStatus

import pytest

SERVICE_AUTH = f"{settings.auth_api_host}:{settings.auth_api_port}"
SERVICE_ROLE = f"{settings.role_api_host}:{settings.role_api_port}"

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

ROLES = [
    {
        "role": "role1",
        "description": "test",
        "rule": "rule1",
    },
    {
        "role": "role2",
        "description": "test",
        "rule": "rule1",
    },
    {
        "role": "role2",
        "description": "test",
        "rule": "rule2",
    },
]

ADMIN_ROLE = {
    "role": "admin",
    "description": "test",
    "rule": "admin",
}

ADMIN_USER = {
    "login": os.environ.get("ADMIN_LOGIN"),
    "password": os.environ.get("ADMIN_PASSWORD"),
}


async def test_role_lifecicle(make_request):
    # login as admin
    response = await make_request(SERVICE_AUTH, "POST", "login", ADMIN_USER)

    assert response.status in [HTTPStatus.OK]
    assert len(response.body) == 2
    assert "access_token" in response.body
    assert "refresh_token" in response.body

    headers = {
        "Authorization": "Bearer " + response.body["access_token"],
    }

    # get all roles
    response = await make_request(SERVICE_ROLE, "GET", "roles", headers=headers)
    assert response.status in [HTTPStatus.OK]
    

    # create role
    response = await make_request(SERVICE_ROLE, "PUT", f"role/{ROLES[0]['role']}", data=ROLES[0], headers=headers)
    assert response.status in [HTTPStatus.OK]
    assert len(response.body) == 0

    # get all roles now only one role
    response = await make_request(SERVICE_ROLE, "GET", "roles", headers=headers)
    roles = response.body
    assert response.status in [HTTPStatus.OK]
    
    assert "role1" == response.body[0]["role"]

    # check this role
    response = await make_request(
        SERVICE_ROLE, "GET", f"role/{roles[0]['id']}", headers=headers
    )
    assert response.status in [HTTPStatus.OK]
    N_ROLES = len(response.body)
    assert response.body["role"] == roles[0]["role"]

    # delete this role
    response = await make_request(
        SERVICE_ROLE, "DELETE", f"role/{roles[0]['id']}", headers=headers
    )
    assert response.status in [HTTPStatus.OK]

    response = await make_request(SERVICE_ROLE, "GET", "roles", headers=headers)
    roles = response.body
    assert response.status in [HTTPStatus.OK]
    N_ROLES -= 1