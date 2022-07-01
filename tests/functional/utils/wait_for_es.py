import urllib.request
import time
import logging

from settings import TestSettings


settings = TestSettings()
ELASTIC_URL = 'http://' + settings.ES_HOST_PORT

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

if __name__ == "__main__":
    connection = False
    while not connection:
        try:
            # Пытаемся прочитать страницу
            contents = urllib.request.urlopen(ELASTIC_URL).read()
        except Exception:
            logging.info("ES: wait for connection")
        else:
            connection = True
            logging.info("ES: successful сonnection")
        time.sleep(5)
