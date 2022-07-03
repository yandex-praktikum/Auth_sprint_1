import pytest

from http import HTTPStatus


pytestmark = pytest.mark.asyncio


async def test_person_id(read_json_data, make_get_request):
    """Проверка выдачи персоны по id"""

    ans_file_path = "/../testdata/ans/persons_id.json"
    ans = await read_json_data(ans_file_path)
    id = ans["uuid"]

    response = await make_get_request("persons/" + id)

    assert response.status == HTTPStatus.OK
    assert response.body == ans


async def test_person_id_404(read_json_data, make_get_request):
    """Проверка выдачи персоны по неправильному id"""

    response_404 = await make_get_request("persons/" + "wrong_id")

    assert response_404.status == HTTPStatus.NOT_FOUND
    assert response_404.body == {"detail": "person not found"}


async def test_person_id_films(read_json_data, make_get_request):
    """Проверка выдачи фильмов персоны"""

    ans_file_path = "/../testdata/ans/persons_id_films.json"
    ans = await read_json_data(ans_file_path)
    id = "e03ce6e9-bfde-4e25-a084-9f7dec951fd8"

    response = await make_get_request("persons/" + id + "/film")

    assert response.status == 200
    assert response.body == ans


async def test_person_id_films_404(read_json_data, make_get_request):
    """Проверка выдачи фильмов персоны по несуществующему id"""

    response_404 = await make_get_request("persons/" + "wrong_id" + "/film")

    assert response_404.status == HTTPStatus.NOT_FOUND
    assert response_404.body == {"detail": "person not found"}


async def test_person_search(read_json_data, make_get_request):
    """Проверка поиска персоны"""

    ans_file_path = "/../testdata/ans/person_search.json"
    ans = await read_json_data(ans_file_path)

    response = await make_get_request("persons/search", {"query": "Morris"})

    assert response.status == 200
    assert len(response.body) == len(ans)
    assert response.body == ans
