import json
import requests


class Pushover:

    def __init__(self):
        self.config = self.load_config()

    @staticmethod
    def load_config():
        with open("pushover_config.json", "r") as f:
            config = json.load(f)
        return config

    def send_message(self, message):
        response = requests.post("https://api.pushover.net/1/messages.json", data={
            "token": self.config["APP_TOKEN"],
            "user": self.config["USER_KEY"],
            "message": message
        })
        print(response.status_code)
        print(response.text)
