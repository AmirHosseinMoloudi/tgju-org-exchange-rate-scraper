import unittest
from unittest.mock import patch, Mock
from json.decoder import JSONDecodeError
import requests # Import for requests.exceptions.RequestException
import io
import contextlib

# Assuming currency_service.py is in the same directory or accessible via PYTHONPATH
from currency_service import get_currency_price, CURRENCY_IDS

class TestCurrencyService(unittest.TestCase):

    def setUp(self):
        # This will be used to capture print statements
        self.captured_output = io.StringIO()
        self.redirect_patch = contextlib.redirect_stdout(self.captured_output)
        self.redirect_patch.__enter__()

    def tearDown(self):
        self.redirect_patch.__exit__(None, None, None)

    @patch('currency_service.requests.get')
    def test_get_price_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        # The item_id in the response is an integer, as observed from actual API
        mock_response.json.return_value = {
            "response": {
                "indicators": [
                    {
                        "item_id": 137206, # Actual API returns int
                        "p": "225310",
                        "title": "درهم امارات "
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        price = get_currency_price("درهم امارات ")
        self.assertEqual(price, "225310")
        # Check that CURRENCY_IDS "137206" (str) is correctly compared with response "137206" (int then str)
        self.assertEqual(CURRENCY_IDS["درهم امارات "], "137206")


    def test_get_price_unknown_currency_name(self):
        price = get_currency_price("خیالی")
        self.assertIsNone(price)
        self.assertIn("Error: Currency 'خیالی' not found in CURRENCY_IDS.", self.captured_output.getvalue())

    @patch('currency_service.requests.get')
    def test_get_price_api_request_exception(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        price = get_currency_price("درهم امارات ")
        self.assertIsNone(price)
        self.assertIn("Error: API request failed: Network error", self.captured_output.getvalue())

    @patch('currency_service.requests.get')
    def test_get_price_api_non_200_status(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Server Error"
        mock_get.return_value = mock_response

        price = get_currency_price("درهم امارات ")
        self.assertIsNone(price)
        self.assertIn("Error: API request failed with status code 500: Server Error", self.captured_output.getvalue())

    @patch('currency_service.requests.get')
    def test_get_price_json_decode_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = JSONDecodeError("JSON error", "doc", 0)
        mock_get.return_value = mock_response

        price = get_currency_price("درهم امارات ")
        self.assertIsNone(price)
        self.assertIn("Error: Failed to parse JSON response: JSON error: line 1 column 1 (char 0)", self.captured_output.getvalue())


    @patch('currency_service.requests.get')
    def test_get_price_item_id_not_in_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "response": {
                "indicators": [
                    {
                        "item_id": 999999, # item_id in response is int
                        "p": "12345",
                        "title": "Some other item"
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        price = get_currency_price("درهم امارات ")
        self.assertIsNone(price)
        self.assertIn("Error: Item ID '137206' not found in API response.", self.captured_output.getvalue())

    @patch('currency_service.requests.get')
    def test_get_price_empty_indicators_list(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": {"indicators": []}}
        mock_get.return_value = mock_response

        price = get_currency_price("درهم امارات ")
        self.assertIsNone(price)
        self.assertIn("Error: Item ID '137206' not found in API response.", self.captured_output.getvalue())

    @patch('currency_service.requests.get')
    def test_get_price_malformed_response_structure_missing_indicators(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": {"not_indicators": []}} # Missing 'indicators'
        mock_get.return_value = mock_response

        price = get_currency_price("درهم امارات ")
        self.assertIsNone(price)
        self.assertIn("Error: Item ID '137206' not found in API response.", self.captured_output.getvalue())

    @patch('currency_service.requests.get')
    def test_get_price_malformed_response_structure_missing_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"foo": "bar"} # Missing 'response'
        mock_get.return_value = mock_response

        price = get_currency_price("درهم امارات ")
        self.assertIsNone(price)
        self.assertIn("Error: Item ID '137206' not found in API response.", self.captured_output.getvalue())


if __name__ == '__main__':
    unittest.main()
