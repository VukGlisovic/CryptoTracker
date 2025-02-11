import time
import logging
from functools import wraps

import yaml


logger = logging.getLogger(__name__)


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config


def retry(max_retries: int = 3, backoff_factor: float = 2., exceptions: tuple = (Exception,)):
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
                    print(f"Attempt {retries + 1} failed: {e}")
                    if retries == max_retries:
                        raise  # Reraise the exception after max retries
                    time.sleep(delay)
                    retries += 1
                    delay *= backoff_factor
            return None

        return wrapper

    return decorator
