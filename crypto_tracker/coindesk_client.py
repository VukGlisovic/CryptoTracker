import os
import requests


class Coindesk:

    def __init__(self):
        self.base_url = "https://api.coindesk.com/v1/"

    def get_current_price(self):
        url = os.path.join(self.base_url, 'bpi/currentprice/EUR.json')
        response = requests.get(url)
        if response.status_code == 200:
            info = response.json()
            return info['bpi']['EUR']['rate_float']
        else:
            print(f"Got status code: {response.status_code} with message:\n{response.text}")
