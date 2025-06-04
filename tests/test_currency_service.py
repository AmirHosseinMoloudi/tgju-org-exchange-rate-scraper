import unittest
import asyncio
from respx import MockRouter

from tgju import ( # Updated to import from the 'tgju' package
    get_currency_price,
    DEFAULT_CURRENCY_IDS,
    DEFAULT_API_BASE_URL,
    # CurrencyError, # Not directly used in current assertions but good to have if needed
    CurrencyAPIError,
    CurrencyNotFoundError
)
import httpx # Required for httpx.RequestError
import json # For json.JSONDecodeError

# Use the actual default IDs from the tgju package for testing
TEST_CURRENCY_IDS = DEFAULT_CURRENCY_IDS.copy()
AED_ITEM_NAME = "درهم امارات " # Define to avoid using string literal repeatedly
AED_ITEM_ID = TEST_CURRENCY_IDS[AED_ITEM_NAME]
API_URL_AED = f"{DEFAULT_API_BASE_URL}{AED_ITEM_ID}" # DEFAULT_API_BASE_URL is also imported


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
                price = await get_currency_price(AED_ITEM_NAME, TEST_CURRENCY_IDS)
                self.assertEqual(price, "225310")
        asyncio.run(run_test())

    def test_get_price_unknown_currency_name(self):
        async def run_test():
            unknown_currency_name = "خیالی"
            with self.assertRaises(CurrencyNotFoundError) as cm:
                await get_currency_price(unknown_currency_name, TEST_CURRENCY_IDS)
            self.assertIn(f"Currency '{unknown_currency_name}' is not defined", str(cm.exception))
        asyncio.run(run_test())

    def test_get_price_api_request_exception(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).mock(side_effect=httpx.RequestError("Network error", request=None))

            with router, self.assertRaises(CurrencyAPIError) as cm:
                await get_currency_price(AED_ITEM_NAME, TEST_CURRENCY_IDS)
            self.assertIn("API request failed", str(cm.exception))
            self.assertIsInstance(cm.exception.__cause__, httpx.RequestError)
        asyncio.run(run_test())

    def test_get_price_api_non_200_status(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(status_code=500, text="Server Error")

            with router, self.assertRaises(CurrencyAPIError) as cm:
                await get_currency_price(AED_ITEM_NAME, TEST_CURRENCY_IDS)
            self.assertIn(f"API request for {AED_ITEM_NAME} failed with status 500: Server Error", str(cm.exception))
            self.assertIsInstance(cm.exception.__cause__, httpx.HTTPStatusError)
        asyncio.run(run_test())

    def test_get_price_json_decode_error(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(status_code=200, content="not a valid json")

            with router, self.assertRaises(CurrencyAPIError) as cm:
                await get_currency_price(AED_ITEM_NAME, TEST_CURRENCY_IDS)
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
                await get_currency_price(AED_ITEM_NAME, TEST_CURRENCY_IDS)
            self.assertIn(f"Item ID '{AED_ITEM_ID}' for '{AED_ITEM_NAME}' not found", str(cm.exception))
        asyncio.run(run_test())

    def test_get_price_empty_indicators_list(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(status_code=200, json={"response": {"indicators": []}})
            with router, self.assertRaises(CurrencyNotFoundError) as cm:
                await get_currency_price(AED_ITEM_NAME, TEST_CURRENCY_IDS)
            self.assertIn(f"Item ID '{AED_ITEM_ID}' for '{AED_ITEM_NAME}' not found", str(cm.exception))
        asyncio.run(run_test())

    def test_get_price_malformed_response_structure_missing_indicators(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(status_code=200, json={"response": {"not_indicators": []}})
            with router, self.assertRaises(CurrencyNotFoundError) as cm:
                await get_currency_price(AED_ITEM_NAME, TEST_CURRENCY_IDS)
            self.assertIn(f"Item ID '{AED_ITEM_ID}' for '{AED_ITEM_NAME}' not found", str(cm.exception))
        asyncio.run(run_test())

    def test_get_price_malformed_response_structure_missing_response(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(status_code=200, json={"foo": "bar"})
            with router, self.assertRaises(CurrencyNotFoundError) as cm:
                await get_currency_price(AED_ITEM_NAME, TEST_CURRENCY_IDS)
            self.assertIn(f"Item ID '{AED_ITEM_ID}' for '{AED_ITEM_NAME}' not found", str(cm.exception))
        asyncio.run(run_test())

    def test_get_price_missing_price_field(self):
        async def run_test():
            router = MockRouter()
            router.get(API_URL_AED).respond(
                status_code=200,
                json={
                    "response": {
                        "indicators": [
                            {"item_id": int(AED_ITEM_ID), "title": AED_ITEM_NAME}
                        ]
                    }
                }
            )
            with router, self.assertRaises(CurrencyNotFoundError) as cm:
                await get_currency_price(AED_ITEM_NAME, TEST_CURRENCY_IDS)
            self.assertIn(f"Price ('p') not found for item ID '{AED_ITEM_ID}'", str(cm.exception))
        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
