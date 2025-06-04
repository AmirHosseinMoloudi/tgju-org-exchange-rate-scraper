import unittest
import asyncio
from respx import MockRouter # Changed from from respx import mock as respx_mock - MockRouter is the new name

from currency_service import (
    get_currency_price,
    DEFAULT_CURRENCY_IDS,
    DEFAULT_API_BASE_URL,
    CurrencyError,
    CurrencyAPIError,
    CurrencyNotFoundError
)
import httpx # Required for httpx.RequestError
import json # For json.JSONDecodeError

# Use the actual default IDs for testing, or define specific test versions if needed
TEST_CURRENCY_IDS = DEFAULT_CURRENCY_IDS.copy()
AED_ITEM_ID = TEST_CURRENCY_IDS["درهم امارات "]
API_URL_AED = f"{DEFAULT_API_BASE_URL}{AED_ITEM_ID}"


class TestCurrencyService(unittest.TestCase):

    def test_get_price_success(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(
                status_code=200,
                json={
                    "response": {
                        "indicators": [
                            {"item_id": int(AED_ITEM_ID), "p": "225310", "title": "درهم امارات "}
                        ]
                    }
                }
            )
            with router:
                price = await get_currency_price("درهم امارات ", TEST_CURRENCY_IDS)
                self.assertEqual(price, "225310")
        asyncio.run(run_test())

    def test_get_price_unknown_currency_name(self):
        async def run_test():
            with self.assertRaises(CurrencyNotFoundError) as cm:
                await get_currency_price("خیالی", TEST_CURRENCY_IDS)
            self.assertIn("Currency 'خیالی' is not defined", str(cm.exception))
        asyncio.run(run_test())

    def test_get_price_api_request_exception(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).mock(side_effect=httpx.RequestError("Network error", request=None)) # request=None for simplicity

            with router, self.assertRaises(CurrencyAPIError) as cm:
                await get_currency_price("درهم امارات ", TEST_CURRENCY_IDS)
            self.assertIn("API request failed", str(cm.exception))
            self.assertIsInstance(cm.exception.__cause__, httpx.RequestError)
        asyncio.run(run_test())

    def test_get_price_api_non_200_status(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(status_code=500, text="Server Error")

            with router, self.assertRaises(CurrencyAPIError) as cm:
                await get_currency_price("درهم امارات ", TEST_CURRENCY_IDS)
            # Note the double space after 'امارات ' due to item_name_to_find having a trailing space
            self.assertIn("API request for درهم امارات  failed with status 500: Server Error", str(cm.exception))
            self.assertIsInstance(cm.exception.__cause__, httpx.HTTPStatusError)
        asyncio.run(run_test())

    def test_get_price_json_decode_error(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(status_code=200, content="not a valid json")

            with router, self.assertRaises(CurrencyAPIError) as cm:
                await get_currency_price("درهم امارات ", TEST_CURRENCY_IDS)
            self.assertIn("Failed to parse JSON response", str(cm.exception))
            self.assertIsInstance(cm.exception.__cause__, json.JSONDecodeError)
        asyncio.run(run_test())

    def test_get_price_item_id_not_in_response(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(
                status_code=200,
                json={
                    "response": {
                        "indicators": [
                            {"item_id": 999999, "p": "12345", "title": "Some other item"}
                        ]
                    }
                }
            )
            with router, self.assertRaises(CurrencyNotFoundError) as cm:
                await get_currency_price("درهم امارات ", TEST_CURRENCY_IDS)
            self.assertIn(f"Item ID '{AED_ITEM_ID}' for 'درهم امارات ' not found", str(cm.exception))
        asyncio.run(run_test())

    def test_get_price_empty_indicators_list(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(status_code=200, json={"response": {"indicators": []}})
            with router, self.assertRaises(CurrencyNotFoundError) as cm:
                await get_currency_price("درهم امارات ", TEST_CURRENCY_IDS)
            self.assertIn(f"Item ID '{AED_ITEM_ID}' for 'درهم امارات ' not found", str(cm.exception))
        asyncio.run(run_test())

    def test_get_price_malformed_response_structure_missing_indicators(self):
        async def run_test():
            router = MockRouter()
            # Response missing 'indicators' key
            router.get(API_URL_AED).respond(status_code=200, json={"response": {"not_indicators": []}})
            with router, self.assertRaises(CurrencyNotFoundError) as cm: # Expecting graceful handling
                await get_currency_price("درهم امارات ", TEST_CURRENCY_IDS)
            self.assertIn(f"Item ID '{AED_ITEM_ID}' for 'درهم امارات ' not found", str(cm.exception))
        asyncio.run(run_test())

    def test_get_price_malformed_response_structure_missing_response(self):
        async def run_test():
            router = MockRouter()
            # Response missing 'response' key
            router.get(API_URL_AED).respond(status_code=200, json={"foo": "bar"})
            with router, self.assertRaises(CurrencyNotFoundError) as cm: # Expecting graceful handling
                await get_currency_price("درهم امارات ", TEST_CURRENCY_IDS)
            self.assertIn(f"Item ID '{AED_ITEM_ID}' for 'درهم امارات ' not found", str(cm.exception))
        asyncio.run(run_test())

    def test_get_price_missing_price_field(self): # New test case
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(
                status_code=200,
                json={
                    "response": {
                        "indicators": [
                            # Price field 'p' is missing
                            {"item_id": int(AED_ITEM_ID), "title": "درهم امارات "}
                        ]
                    }
                }
            )
            with router, self.assertRaises(CurrencyNotFoundError) as cm:
                await get_currency_price("درهم امارات ", TEST_CURRENCY_IDS)
            self.assertIn(f"Price ('p') not found for item ID '{AED_ITEM_ID}'", str(cm.exception))
        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
