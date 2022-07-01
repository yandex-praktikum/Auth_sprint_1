#!/bin/sh

# run tests
python3 /tests/functional/utils/wait_for_es.py
python3 /tests/functional/utils/wait_for_redis.py
python3 /tests/functional/utils/wait_for_fastapi.py
pytest /tests/functional/search_api/src --log-format="%(asctime)s %(levelname)s %(message)s"
pytest /tests/functional/role_api/src --log-format="%(asctime)s %(levelname)s %(message)s"
pytest /tests/functional/auth_api/src --log-format="%(asctime)s %(levelname)s %(message)s"

exec "$@"