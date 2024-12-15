import time

from crypto_tracker.coindesk_client import Coindesk
from crypto_tracker.pushover_client import Pushover


def main():
    client_coindesk = Coindesk()
    client_pushover = Pushover()

    while True:
        value = client_coindesk.get_current_price()
        message = f"Bitcoin value: €{value}"
        print(message)
        client_pushover.send_message(message)
        time.sleep(30)


if __name__ == '__main__':
    main()
