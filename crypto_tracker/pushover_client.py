import logging
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta

from crypto_tracker.utils import load_config, retry


logger = logging.getLogger(__name__)


class Pushover:

    def __init__(self):
        self.config = load_config("configs/pushover_config.yaml")
        self.cooldown = self.config['cooldown']
        self.last_message_sent = datetime.now() - relativedelta(seconds=self.cooldown)  # init sothat a message can be sent immediately

    @retry(max_retries=5, backoff_factor=2)
    def send_message(self, message: str) -> None:
        if datetime.now() < self.last_message_sent + relativedelta(seconds=self.cooldown):
            # too soon to send another message
            return
        response = requests.post("https://api.pushover.net/1/messages.json", data={
            "token": self.config["app_token"],
            "user": self.config["user_key"],
            "message": message
        })
        self.last_message_sent = datetime.now()
        logger.info(f"Sent pushover message: {message}")

        if response.status_code != 200:
            logger.error(f"Got status code: {response.status_code} with message:\n{response.text}")
