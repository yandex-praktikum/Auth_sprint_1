import pytest

from http import HTTPStatus


pytestmark = pytest.mark.asyncio


async def test_genres_id(read_json_data, make_get_request):
    """Проверка выдачи жанра по id"""

    ans_file_path = "/../testdata/ans/genres_id.json"
    ans = await read_json_data(ans_file_path)
    id = ans["uuid"]

    response = await make_get_request("genres/" + id)

    assert response.status == HTTPStatus.OK
    assert response.body == ans


async def test_genres_id_404(read_json_data, make_get_request):
    """Проверка выдачи жанра по неправильному id"""

    response_404 = await make_get_request("genres/" + "wrong_id")

    assert response_404.status == HTTPStatus.NOT_FOUND
    assert response_404.body == {"detail": "genre not found"}


async def test_genres(read_json_data, fill_elastic_data, make_get_request):
    """Проверка выдачи жанров"""

    ans_file_path = "/../testdata/ans/genres.json"
    ans = await read_json_data(ans_file_path)

    response = await make_get_request("genres")

    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(ans)
    assert response.body == ans
