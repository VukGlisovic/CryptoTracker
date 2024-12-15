import time

from crypto_tracker.coindesk_client import Coindesk


def main():
    client = Coindesk()

    while True:
        value = client.get_current_price()
        print(value)
        time.sleep(5)


if __name__ == '__main__':
    main()
