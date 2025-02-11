import unittest
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from crypto_tracker.strike_client import Strike, relativedelta, load_config, BTC_EUR


class TestStrikeClient(unittest.TestCase):

    @patch('crypto_tracker.strike_client.load_config')
    @patch('pandas.read_csv')
    @patch('os.path.exists')
    def setUp(self, mock_path_exists, mock_read_csv, mock_load_config):
        """Setup method to create an instance of Strike before each test."""
        self.mock_config = {
            "api_key": "test_api_key"
        }
        mock_path_exists.return_value = True
        now = datetime.now()
        mock_read_csv.return_value = pd.DataFrame(
            data={BTC_EUR: [30000, 40000, 50000]},
            index=[now - relativedelta(days=2), now - relativedelta(days=1), now]
        )
        mock_load_config.return_value = self.mock_config
        self.strike = Strike()  # Now the Strike instance is created within setUp

    @patch('requests.get')
    def test_get_current_price_success(self, mock_get):
        """Test that get_current_price returns the correct price on success."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'sourceCurrency': 'BTC', 'targetCurrency': 'EUR', 'amount': '30000.00'}]
        mock_get.return_value = mock_response
        price = self.strike.get_current_price(store=False)  # Set store=False to avoid appending to history
        self.assertEqual(price, 30000.0)

    @patch('requests.get')
    def test_get_current_price_failure(self, mock_get):
        """Test that get_current_price handles API request failures."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Error message"
        mock_get.return_value = mock_response
        with self.assertLogs(level='ERROR') as cm:
            price = self.strike.get_current_price(store=False)
        self.assertTrue(np.isnan(price))

    def test_create_daily_update_message(self):
        """Test that create_daily_update_message generates the correct message format."""
        message = self.strike.create_daily_update_message()
        self.assertIn("Current bitcoin value:", message)
        self.assertIn("Spread last 24h:", message)
        self.assertIn("Volatility last 24h:", message)

    def test_create_message_if_value_low(self):
        """Test that create_message_if_value_low generates a message when the value is low."""
        message = self.strike.create_message_if_value_low(5000.0, datetime.now(), 3, 1.0)
        self.assertIn("Bitcoin value is relatively low compared to last 3 days", message)


if __name__ == '__main__':
    unittest.main()
