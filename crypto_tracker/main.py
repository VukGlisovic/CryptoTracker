import sys
import time
import logging
import argparse
from datetime import datetime

from dateutil.relativedelta import relativedelta

from crypto_tracker.utils import load_config
from crypto_tracker.strike_client import Strike
from crypto_tracker.pushover_client import Pushover


def main(config: dict) -> None:
    # unpack config
    frac = config['main']['frac']
    days_hist = config['main']['days_hist']
    freq = config['main']['freq']
    update_hour = config['main']['update_hour']

    # init clients
    client_strike = Strike()
    client_pushover = Pushover(**config['pushover'])

    # setup stateful variables
    day_last_update_value = datetime.now().day

    while True:
        # get starting time of this iteration
        now = datetime.now()

        # get current price and check if message needs to be sent
        value = client_strike.get_current_price(store=True)
        start, end = now - relativedelta(days=days_hist), datetime(now.year, now.month, now.day)
        if not client_strike.history.loc[start: end].empty and value < frac * min(client_strike.history.loc[start: end]):
            message = f"Bitcoin value: €{value}"
            client_pushover.send_message(message)

        # check if it's time for the daily update
        if day_last_update_value != now.day and now.hour == update_hour:
            message = f"Bitcoin value: €{client_strike.history[-1]}"
            client_pushover.send_message(message)
            day_last_update_value = now.day

        time.sleep(freq)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config_path', default='configs/main_config.yaml', type=str, help="Config for the entire application.")
    args, _ = parser.parse_known_args()

    # Configure the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(handler)

    main(
        load_config(args.config_path)
    )
