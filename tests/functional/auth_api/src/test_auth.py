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

async def test_signup(read_json_data, make_request):
    USERS[0]["login"] += str(time.time())
    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    logger.info(response)
    assert response.status in [HTTPStatus.CREATED]
    assert response.body == {}

async def test_signup_or_user_exist(read_json_data, make_request):
    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    logger.info(response)
    assert response.status in [HTTPStatus.CREATED, HTTPStatus.CONFLICT]
    assert response.body == {}


async def test_signup_and_login_if_user_exist(read_json_data, make_request):
    response = await make_request(SERVICE, "POST", "signup", USERS[0])
    logger.info(response)
    assert response.status in [HTTPStatus.CREATED, HTTPStatus.CONFLICT]
    assert response.body == {}

    login_info = {
        "login": USERS[0]["login"],
        "password": USERS[0]["password"],
    }
    response = await make_request(SERVICE, "POST", "login", login_info)
    logger.info(response)
    assert response.status in [HTTPStatus.ACCEPTED]
    assert len(response.body) == 2
    assert "access_token" in response.body
    assert "refresh_token" in response.body




# async def test_film_id_404(read_json_data, make_get_request):
#     """Проверка выдачи фильма по несуществующему id"""

#     response_404 = await make_get_request('films/'+'wrong_id')

#     assert response_404.status == HTTPStatus.NOT_FOUND
#     assert response_404.body == {'detail': 'film not found'}


# async def test_film_sort(read_json_data, make_get_request):
#     """Проверка сортировки фильмов"""

#     ans_path = '/../testdata/ans/film_sort.json'
#     ans = await read_json_data(ans_path)

#     response = await make_get_request('films', {'sort': '-imdb_rating'})
    
#     assert response.status == HTTPStatus.OK
#     assert len(response.body) == 20
#     assert response.body == ans

    
# async def test_film_sort_400(read_json_data, make_get_request):
#     """Проверка сортировки фильмов с невалидным запросом"""

#     response_400 = await make_get_request('films', {'sort': 'wrong_rating'})

#     assert response_400.status == HTTPStatus.BAD_REQUEST
#     assert response_400.body == {'detail': 'wrong request'}


# async def test_film_sort_qenre(read_json_data, make_get_request):
#     """Проверка сортировки по жанру"""

#     ans_path = '/../testdata/ans/film_sort_genre.json'
#     ans = await read_json_data(ans_path)

#     response = await make_get_request('films', {
#         'sort': '-imdb_rating',
#         'genre': 'b92ef010-5e4c-4fd0-99d6-41b6456272cd'
#     })

#     assert response.status == 200
#     assert len(response.body) == len(ans)
#     assert response.body == ans


# async def test_film_sort_qenre_3(read_json_data, make_get_request):
#     """Проверка сортировки по жанру с ограниченной выдачей"""

#     ans_path = '/../testdata/ans/film_sort_genre.json'
#     ans = await read_json_data(ans_path)

#     response_3 = await make_get_request('films', {
#         'sort': '-imdb_rating',
#         'genre': 'b92ef010-5e4c-4fd0-99d6-41b6456272cd',
#         'page[size]': '3',
#         'page[number]': '1'
#     })

#     assert response_3.status == 200
#     assert len(response_3.body) == 3
#     assert response_3.body == ans[0:3]


# async def test_film_sort_qenre_400_sort(read_json_data, make_get_request):
#     """Проверка сортировки по жанру с ошибкой в сортировке"""

#     response_400_sort = await make_get_request('films', {
#         'sort': 'wrong_rating',
#         'genre': 'b92ef010-5e4c-4fd0-99d6-41b6456272cd'
#     })

#     assert response_400_sort.status == HTTPStatus.BAD_REQUEST
#     assert response_400_sort.body == {'detail': 'wrong request'}


# async def test_film_sort_qenre_400_genre(read_json_data, make_get_request):
#     """Проверка сортировки по жанру с ошибкой в жанре"""

#     response_400_genre = await make_get_request('films', {
#         'sort': '-imdb_rating',
#         'genre': 'wrong_genre'
#     })

#     assert response_400_genre.status == HTTPStatus.BAD_REQUEST
#     assert response_400_genre.body == {'detail': 'wrong request'}


# async def test_film_search(read_json_data, make_get_request):
#     """Проверка поиска по фильмам"""

#     # Подготовка
#     ans_path = '/../testdata/ans/film_search.json'
#     ans = await read_json_data(ans_path)

#     # Вызов тестируемой функции
#     response = await make_get_request('films/search', {'query': 'Star Wars'})

#     # Проверки
#     assert response.status == 200
#     assert len(response.body) == len(ans)
#     assert response.body == ans
