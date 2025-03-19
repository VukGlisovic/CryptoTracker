import time
import logging
from functools import wraps
from typing import Callable

import yaml


logger = logging.getLogger(__name__)


def retry(max_retries: int = 3, backoff_factor: float = 2., exceptions: tuple = (Exception,)) -> Callable:
    """Decorator to retry a function with exponential backoff.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = 1
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.info(f"Attempt {retries + 1} failed: {e}")
                    if retries == max_retries:
                        raise  # Reraise the exception after max retries
                    time.sleep(delay)
                    retries += 1
                    delay *= backoff_factor
            return None

        return wrapper

    return decorator
