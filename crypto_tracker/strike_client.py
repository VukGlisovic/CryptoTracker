import logging
import os.path
from datetime import datetime

import requests
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

from crypto_tracker.constants import BTC_EUR
from crypto_tracker.utils import load_config, retry


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
            self.history = pd.DataFrame(data={BTC_EUR: [self.get_current_price()]}, index=[datetime.now()])
            self.history.index.name = 'date'
            self.history.to_csv(self.ticker_path, index=True)

    def append_to_history(self, price: float) -> None:
        now = datetime.now()
        with open(self.ticker_path, 'a') as f:
            f.write(f"{now},{price}\n")
        self.history.loc[now] = {BTC_EUR: price}

    @retry(max_retries=5, backoff_factor=2)
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

    def create_daily_update_message(self) -> str:
        end = datetime.now()
        start = end - relativedelta(days=1)
        data_last_24h = self.history.loc[start: end, BTC_EUR]
        message = (f"Current bitcoin value: €{self.history[BTC_EUR].iloc[-1]}\n"
                   f"Spread last 24h: €{data_last_24h.min()} - €{data_last_24h.max()}\n"
                   f"Volatility last 24h: €{data_last_24h.std():.2f}")
        return message

    def create_message_if_value_low(self, value: float, now: datetime, days_hist: int, n_std: float) -> str:
        start, end = now - relativedelta(days=days_hist), datetime(now.year, now.month, now.day)
        if self.history.loc[start: end].empty:
            return ""
        mean, std = self.history.loc[start: end, BTC_EUR].agg(['mean', 'std'])
        if value < mean - n_std * std:
            message = (f"Bitcoin value is relatively low compared to last {days_hist} days: €{value}.\n"
                       f"mean - n_std * std = {mean} - {n_std} * {std} = €{mean - n_std * std} > €{value}")
        else:
            message = ""
        return message
