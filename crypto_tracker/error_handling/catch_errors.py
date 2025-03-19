import time
import logging
from functools import wraps
from typing import Callable

import yaml

from crypto_tracker.pushover_client import Pushover


logger = logging.getLogger(__name__)


def catch_function_errors(fnc: Callable) -> Callable:

    pushover_client = Pushover()

    def wrapper(*args, **kwargs):
        try:
            return fnc(*args, **kwargs)
        except KeyboardInterrupt:
            pushover_client.send_message("KeyboardInterrupt stopped the script.", force_send=True)
        except Exception as e:
            logger.exception(e)
            pushover_client.send_message("CryptoTracker exited.", force_send=True)

    return wrapper
