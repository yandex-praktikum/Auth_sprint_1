#!/bin/sh

# run tests
cd /tests/functional
python3 ./utils/wait_for_service.py es
python3 ./utils/wait_for_service.py redis
python3 ./utils/wait_for_service.py postgres
python3 ./utils/wait_for_service.py auth_api
python3 ./utils/wait_for_service.py role_api
python3 ./utils/wait_for_service.py search_api
# pytest ./search_api/src --log-format="%(asctime)s %(levelname)s %(message)s"
# pytest ./role_api/src --log-format="%(asctime)s %(levelname)s %(message)s"
pytest ./auth_api/src --log-format="%(asctime)s %(levelname)s %(message)s"

exec "$@"