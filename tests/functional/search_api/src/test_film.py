from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_film_id(read_json_data, make_get_request):
    """Проверка выдачи фильма по id"""

    ans_file_path = "/../testdata/ans/film_id.json"
    ans = await read_json_data(ans_file_path)
    id = ans["uuid"]

    response = await make_get_request("films/" + id)

    assert response.status == HTTPStatus.OK
    assert response.body == ans


async def test_film_id_404(read_json_data, make_get_request):
    """Проверка выдачи фильма по несуществующему id"""

    response_404 = await make_get_request("films/" + "wrong_id")

    assert response_404.status == HTTPStatus.NOT_FOUND
    assert response_404.body == {"detail": "film not found"}


async def test_film_sort(read_json_data, make_get_request):
    """Проверка сортировки фильмов"""

    ans_path = "/../testdata/ans/film_sort.json"
    ans = await read_json_data(ans_path)

    response = await make_get_request("films", {"sort": "-imdb_rating"})

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 20
    assert response.body == ans


async def test_film_sort_400(read_json_data, make_get_request):
    """Проверка сортировки фильмов с невалидным запросом"""

    response_400 = await make_get_request("films", {"sort": "wrong_rating"})

    assert response_400.status == HTTPStatus.BAD_REQUEST
    assert response_400.body == {"detail": "wrong request"}


async def test_film_sort_qenre(read_json_data, make_get_request):
    """Проверка сортировки по жанру"""

    ans_path = "/../testdata/ans/film_sort_genre.json"
    ans = await read_json_data(ans_path)

    response = await make_get_request(
        "films",
        {"sort": "-imdb_rating", "genre": "b92ef010-5e4c-4fd0-99d6-41b6456272cd"},
    )

    assert response.status == 200
    assert len(response.body) == len(ans)
    assert response.body == ans


async def test_film_sort_qenre_3(read_json_data, make_get_request):
    """Проверка сортировки по жанру с ограниченной выдачей"""

    ans_path = "/../testdata/ans/film_sort_genre.json"
    ans = await read_json_data(ans_path)

    response_3 = await make_get_request(
        "films",
        {
            "sort": "-imdb_rating",
            "genre": "b92ef010-5e4c-4fd0-99d6-41b6456272cd",
            "page[size]": "3",
            "page[number]": "1",
        },
    )

    assert response_3.status == 200
    assert len(response_3.body) == 3
    assert response_3.body == ans[0:3]


async def test_film_sort_qenre_400_sort(read_json_data, make_get_request):
    """Проверка сортировки по жанру с ошибкой в сортировке"""

    response_400_sort = await make_get_request(
        "films",
        {"sort": "wrong_rating", "genre": "b92ef010-5e4c-4fd0-99d6-41b6456272cd"},
    )

    assert response_400_sort.status == HTTPStatus.BAD_REQUEST
    assert response_400_sort.body == {"detail": "wrong request"}


async def test_film_sort_qenre_400_genre(read_json_data, make_get_request):
    """Проверка сортировки по жанру с ошибкой в жанре"""

    response_400_genre = await make_get_request(
        "films", {"sort": "-imdb_rating", "genre": "wrong_genre"}
    )

    assert response_400_genre.status == HTTPStatus.BAD_REQUEST
    assert response_400_genre.body == {"detail": "wrong request"}


async def test_film_search(read_json_data, make_get_request):
    """Проверка поиска по фильмам"""

    # Подготовка
    ans_path = "/../testdata/ans/film_search.json"
    ans = await read_json_data(ans_path)

    # Вызов тестируемой функции
    response = await make_get_request("films/search", {"query": "Star Wars"})

    # Проверки
    assert response.status == 200
    assert len(response.body) == len(ans)
    assert response.body == ans
