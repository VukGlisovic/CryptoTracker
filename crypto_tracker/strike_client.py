import logging
import os.path
from datetime import datetime

import requests
import numpy as np
import pandas as pd

from crypto_tracker.utils import load_config


logger = logging.getLogger(__name__)


class Strike:

    def __init__(self):
        self.base_url = "https://api.strike.me/v1"
        self.config = load_config("configs/strike_config.yaml")
        self.ticker_path = 'data/btc-eur.csv'
        if os.path.exists(self.ticker_path):
            self.history = pd.read_csv(self.ticker_path, index_col='date')
            self.history.index = pd.to_datetime(self.history.index)
        else:
            if d := os.path.dirname(self.ticker_path):
                os.makedirs(d, exist_ok=True)
            self.history = pd.DataFrame(data={'btc-eur': [self.get_current_price()]}, index=[datetime.now()])
            self.history.index.name = 'date'
            self.history.to_csv(self.ticker_path, index=True)

    def append_to_history(self, price):
        now = datetime.now()
        logger.info(f"Storing price {price} at time {now}")
        with open(self.ticker_path, 'a') as f:
            f.write(f"{now},{price}\n")
        self.history.loc[now] = {'btc-eur': price}

    def get_current_price(self, source_currency: str = 'BTC', target_currency: str = 'EUR', store: bool = False) -> float:
        url = f"{self.base_url}/rates/ticker"

        payload = {}
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers, data=payload)
        if response.status_code == 200:
            rate = [r for r in response.json() if r['sourceCurrency'] == source_currency and r['targetCurrency'] == target_currency][0]
            price = float(rate['amount'])
        else:
            logger.error(f"Got status code: {response.status_code} with message:\n{response.text}")
            price = np.NaN

        if store:
            self.append_to_history(price)

        return price
