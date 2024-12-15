from typing import Optional
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta


class Coindesk:

    def __init__(self):
        self.base_url = "https://api.coindesk.com/v1"
        self.history = []

    def update_history(self, start: Optional[str] = None, end: Optional[str] = None):
        """
        Format of start and end: yyyy-mm-dd.
        If no start and end provided, it takes the last 3 months of data.
        """
        if start is None or end is None:
            now = datetime.now()
            end = now.strftime("%Y-%m-%d")
            start = (now - relativedelta(months=3)).strftime("%Y-%m-%d")
        url = f"{self.base_url}/bpi/historical/EUR.json?start={start}&end={end}"
        response = requests.get(url)
        if response.status_code == 200:
            info = response.json()
            history = info['bpi']
            dates = sorted(history.keys())
            values = [history[d] for d in dates]
            return values

    def get_current_price(self):
        url = f"{self.base_url}/bpi/currentprice/EUR.json"
        response = requests.get(url)
        if response.status_code == 200:
            info = response.json()
            return info['bpi']['EUR']['rate_float']
        else:
            print(f"Got status code: {response.status_code} with message:\n{response.text}")
