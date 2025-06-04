"""Fetches live currency prices using the TGJU API.

This module provides functionality to retrieve the live price of specified currencies
(e.g., "درهم امارات ") by querying an external API (tgju.org). It uses `httpx`
for asynchronous HTTP requests and `asyncio` for managing asynchronous operations.

Main components:
- `get_currency_price()`: An asynchronous function that fetches the price for a
  given currency name. It requires a mapping of currency names to their API item IDs.
- Custom Exceptions:
    - `CurrencyError`: Base exception for this module.
    - `CurrencyAPIError`: For issues related to API communication (network, HTTP errors).
    - `CurrencyNotFoundError`: When a currency definition or its data isn't found.
- Configuration:
    - `DEFAULT_CURRENCY_IDS`: A default mapping of currency names to item IDs.
    - `DEFAULT_API_BASE_URL`: The default base URL for the TGJU API.

The module can be run as a script for a simple demonstration, which will fetch
the price of "درهم امارات " and log the outcome.
"""

import httpx
import asyncio
import logging
import json # For json.JSONDecodeError
from typing import Dict

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

# Create a module-level logger instance
logger: logging.Logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CURRENCY_IDS: Dict[str, str] = {"درهم امارات ": "137206"}
DEFAULT_API_BASE_URL: str = "https://api.tgju.org/v1/widget/tmp?keys="

# Custom Exception Classes
class CurrencyError(Exception):
    """Base class for exceptions raised by the currency_service module."""
    pass

class CurrencyAPIError(CurrencyError):
    """Raised for errors related to the external currency API.

    This can include network issues, HTTP error status codes from the API,
    or problems decoding the API's JSON response.
    """
    pass

class CurrencyNotFoundError(CurrencyError):
    """Raised when a currency's definition or its data cannot be found.

    This can occur if the requested currency name is not in the provided
    currency IDs map, or if the API response does not contain the expected
    item ID or price information.
    """
    pass

async def get_currency_price(
    item_name_to_find: str,
    currency_ids: Dict[str, str],
    base_api_url: str = DEFAULT_API_BASE_URL
) -> str:
    """Fetches the live price for a specified currency item.

    This function asynchronously queries the TGJU API to retrieve the price
    of a currency item identified by its name.

    Args:
        item_name_to_find: The common name of the currency to fetch.
                           Must be a key in the `currency_ids` dictionary.
        currency_ids: A dictionary mapping currency names to their unique
                      item IDs (strings).
        base_api_url: The base URL for the TGJU API endpoint. Defaults to
                      `DEFAULT_API_BASE_URL`.

    Returns:
        str: The price of the currency as a string.

    Raises:
        CurrencyNotFoundError: If `item_name_to_find` is not in `currency_ids`,
                               or if the item ID or its price is not found in
                               the API response.
        CurrencyAPIError: If there's an issue with the API request (network error,
                          HTTP error status, JSON decoding error).
    """
    if item_name_to_find not in currency_ids:
        raise CurrencyNotFoundError(f"Currency '{item_name_to_find}' is not defined in the provided currency IDs map.")

    item_id: str = currency_ids[item_name_to_find]
    api_url: str = f"{base_api_url}{item_id}"

    async with httpx.AsyncClient() as client:
        try:
            response: httpx.Response = await client.get(api_url)
            response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx responses
            data: dict = response.json()
        except httpx.HTTPStatusError as e:
            raise CurrencyAPIError(f"API request for {item_name_to_find} failed with status {e.response.status_code}: {e.response.text}") from e
        except httpx.RequestError as e:
            raise CurrencyAPIError(f"API request failed for {item_name_to_find}: {e}") from e
        except json.JSONDecodeError as e: # Catching the standard JSONDecodeError
            raise CurrencyAPIError(f"Failed to parse JSON response for {item_name_to_find}: {e}") from e

    indicators: list = data.get("response", {}).get("indicators", [])

    for indicator_data in indicators:
        if str(indicator_data.get("item_id")) == item_id:
            price: str | None = indicator_data.get("p")
            if price is None:
                raise CurrencyNotFoundError(f"Price ('p') not found for item ID '{item_id}' ({item_name_to_find}) in API response.")
            return price

    raise CurrencyNotFoundError(f"Item ID '{item_id}' for '{item_name_to_find}' not found in API response indicators.")

async def main_async():
    """Runs a demonstration of the currency price fetching service.

    This function attempts to fetch the price for a known currency ("درهم امارات ")
    and a currency that is intentionally not defined in the default map ("خیالی"),
    logging the outcomes. It serves as the main entry point when the script is
    executed directly.
    """
    # Test successful retrieval
    try:
        aed_price: str = await get_currency_price("درهم امارات ", DEFAULT_CURRENCY_IDS)
        logger.info(f"The price of درهم امارات is: {aed_price}")
    except CurrencyNotFoundError as e:
        logger.error(f"Could not find currency data for درهم امارات: {e}")
    except CurrencyAPIError as e:
        logger.error(f"API error when fetching price for درهم امارات: {e}")
    except CurrencyError as e: # Catch any other custom errors from this module
        logger.error(f"An unexpected currency error occurred for درهم امارات: {e}")


if __name__ == "__main__":
    asyncio.run(main_async())
