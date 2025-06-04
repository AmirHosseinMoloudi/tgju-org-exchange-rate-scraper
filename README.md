# TGJU Currency Price Fetcher

This Python module, `currency_service.py`, asynchronously fetches the live price of specified currencies from an external API (tgju.org). It utilizes `httpx` for non-blocking API calls and `asyncio` for managing asynchronous operations. It's currently configured by default to retrieve the price for "درهم امارات " (AED).

## Features

-   Asynchronously fetches live currency prices using `httpx`.
-   Parses JSON responses from the API.
-   Implements robust error handling using custom exceptions:
    -   `CurrencyAPIError`: For issues related to API communication (network errors, HTTP errors, JSON parsing failures).
    -   `CurrencyNotFoundError`: When a currency definition or its specific data isn't found.
-   Uses Python's `logging` module for informative output and error reporting.
-   Allows configuration of currency item IDs and the API base URL.
-   Comes with a comprehensive unit test suite using `unittest` and `respx` (for mocking `httpx` calls).
-   Includes setup and run scripts for both Linux/macOS and Windows.

## Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    # git clone <repository-url>
    # cd <repository-directory>
    ```

2.  **Automated Setup (Recommended):**
    These scripts will attempt to create a Python virtual environment in a directory named `venv` and install the required dependencies from `requirements.txt`.
    *   **For Linux/macOS:**
        ```bash
        chmod +x setup.sh
        ./setup.sh
        ```
    *   **For Windows:**
        ```bat
        setup.bat
        ```

3.  **Manual Setup:**
    If you prefer to set up manually or the scripts encounter issues:
    *   **Create a virtual environment (recommended):**
        ```bash
        python -m venv venv
        ```
    *   **Activate the virtual environment:**
        *   Linux/macOS: `source venv/bin/activate`
        *   Windows: `venv\Scripts\activate`
    *   **Install dependencies:**
        The `requirements.txt` file includes `httpx` for the core functionality and `respx` for running the test suite.
        ```bash
        pip install -r requirements.txt
        ```

## Usage

Ensure your virtual environment is activated if you are not using the provided run scripts (e.g., `source venv/bin/activate` or `venv\Scripts\activate`).

### As a Module

The primary function `get_currency_price` is an asynchronous function. You'll need to run it within an asyncio event loop.

**Function Signature:**
```python
async def get_currency_price(
    item_name_to_find: str,
    currency_ids: Dict[str, str],
    base_api_url: str = DEFAULT_API_BASE_URL
) -> str:
```
-   `item_name_to_find` (str): The common name of the currency (must be a key in `currency_ids`).
-   `currency_ids` (Dict[str, str]): A dictionary mapping currency names to their API item IDs.
-   `base_api_url` (str, optional): The base URL for the API. Defaults to `DEFAULT_API_BASE_URL` from the module.

**Returns:**
-   `str`: The price of the currency as a string.

**Raises:**
-   `CurrencyNotFoundError`: If the currency name isn't in `currency_ids`, or if its data/price isn't in the API response.
-   `CurrencyAPIError`: For API communication issues (network, HTTP errors, JSON parsing).

**Example:**
```python
import asyncio
import logging
from currency_service import (
    get_currency_price,
    DEFAULT_CURRENCY_IDS,
    DEFAULT_API_BASE_URL, # Can be used or overridden
    CurrencyError # Base exception, can catch CurrencyAPIError and CurrencyNotFoundError
)

# Configure a basic logger if you want to see logs from the example itself
# The currency_service module already configures its own logger.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def fetch_example_prices():
    # Example 1: Fetching a known currency
    try:
        # Using default currency IDs and API URL from the module
        aed_price = await get_currency_price("درهم امارات ", DEFAULT_CURRENCY_IDS)
        logger.info(f"Successfully fetched AED price: {aed_price}")
    except CurrencyError as e:
        logger.error(f"Error fetching AED price: {e}")

    # Example 2: Attempting to fetch a currency not in DEFAULT_CURRENCY_IDS
    try:
        unknown_price = await get_currency_price("خیالی", DEFAULT_CURRENCY_IDS)
        logger.info(f"Price of خیالی: {unknown_price}") # Should not be reached
    except CurrencyNotFoundError as e:
        logger.error(f"Expected error fetching 'خیالی': {e}")
    except CurrencyAPIError as e: # Should not be this error for 'خیالی' if defined locally
        logger.error(f"API error for 'خیالی': {e}")


if __name__ == "__main__":
    asyncio.run(fetch_example_prices())
```

### Using Run Scripts (Demo)

The provided run scripts activate the virtual environment (if found) and execute `currency_service.py` directly. The script uses `asyncio.run()` to call its `main_async()` function, which demonstrates fetching "درهم امارات " and handling potential errors. Output, including logs, will be printed to the console. These scripts now invoke python with the `-B` flag to prevent `__pycache__` creation.

*   **For Linux/macOS:**
    ```bash
    chmod +x run.sh
    ./run.sh
    ```
*   **For Windows:**
    ```bat
    run.bat
    ```

### Manual Execution (Demo)

To see the demonstration by running the `currency_service.py` script directly (ensure virtual environment is active):

```bash
python -B currency_service.py
```
This will print log output regarding the fetching of "درهم امارات " to the console.

## Configuration

The `currency_service.py` module defines the following default configurations:
-   `DEFAULT_CURRENCY_IDS: Dict[str, str]`: A dictionary mapping commonly known currency names to their TGJU API item IDs. Currently, it only contains "درهم امارات ".
    ```python
    DEFAULT_CURRENCY_IDS = {"درهم امارات ": "137206"}
    ```
-   `DEFAULT_API_BASE_URL: str`: The base URL for the TGJU API endpoint used.
    ```python
    DEFAULT_API_BASE_URL = "https://api.tgju.org/v1/widget/tmp?keys="
    ```
You can customize the behavior by:
1.  Modifying these constants directly in the script (not recommended for library use).
2.  Passing your own `currency_ids` dictionary and/or `base_api_url` string when calling the `get_currency_price` function. This is the preferred method for flexibility.

## Running Tests

Unit tests are located in `test_currency_service.py` and use Python's `unittest` module. They have been updated to test asynchronous operations and use the `respx` library to mock `httpx` API calls.

To run the tests (ensure virtual environment is active and `respx` is installed via `requirements.txt`):

```bash
python -m unittest test_currency_service.py
```
Alternatively, for test discovery (though the command above is more direct for a single test file):
```bash
python -m unittest discover
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
