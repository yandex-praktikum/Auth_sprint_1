import logging
import sys
import time
import traceback
from collections.abc import Callable
from functools import wraps
from logging import Logger
from typing import NoReturn

logger = logging.getLogger()


class BackoffFailException(Exception):
    pass


def handle_errors(err: Exception) -> NoReturn:
    """Handle errors for sqlite3."""
    logger.error("Error: %s" % (" ".join(err.args)))
    logger.error("Exception class is: %s" % err.__class__)
    logger.error("Traceback: ")
    exc_type, exc_value, exc_tb = sys.exc_info()
    logger.error(traceback.format_exception(exc_type, exc_value, exc_tb))


def backoff(
    func: Callable,
    initial: float = 0.1,
    factor: int = 2,
    max_timeout: int = 3,
    max_tries: int = 10,
    logger: Logger = logger,
) -> Callable:
    """Backoff functional decorator."""

    @wraps(func)
    def inner(*args, **kwargs):
        timeout = initial
        attempts = 0
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as err:
                handle_errors(err)
                time.sleep(timeout)
                timeout = min(initial * (attempts**factor), max_timeout)
                logger.error(
                    f"Backoff attempt fail with timeout \
{timeout}, {err}"
                )
                attempts += 1
                continue
            finally:
                if attempts == max_tries:
                    logger.error("Too many attempts in a backoff decorator")
                    raise BackoffFailException(
                        "Too many attempts in a backoff decorator"
                    )

    return inner
