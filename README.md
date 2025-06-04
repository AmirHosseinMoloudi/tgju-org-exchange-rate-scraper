https://pypi.org/project/tgju/
[![PyPI version](https://img.shields.io/pypi/v/tgju.svg)](https://pypi.org/project/tgju/)

# TGJU Currency Price Fetcher

The `tgju` Python package provides an asynchronous client to fetch live prices of specified currencies and other assets by querying an external API (tgju.org). It is built using `httpx` for non-blocking API calls and `asyncio` for managing asynchronous operations.

By default, the package can retrieve the price for "درهم امارات " (AED), but it is configurable to fetch other items if their API item IDs are known.

## Project Structure

The project is organized as follows:

```
tgju/
├── src/
│   └── tgju/
│       ├── __init__.py           # Makes 'tgju' a package, exports main functions
│       └── currency_service.py   # Core logic for fetching currency prices
├── tests/
│   └── test_currency_service.py  # Unit tests
├── .gitignore
├── LICENSE                       # MIT License file
├── README.md                     # This file
├── pyproject.toml                # PEP 621 package metadata and build configuration
├── requirements.txt              # Development, test, and build dependencies
├── run.bat                       # Windows script to run demo
├── run.sh                        # Linux/macOS script to run demo
├── setup.bat                     # Windows script for development environment setup
└── setup.sh                      # Linux/macOS script for development environment setup
```

## Features

-   Asynchronously fetches live currency prices using `httpx`.
-   Parses JSON responses from the API.
-   Implements robust error handling using custom exceptions:
    -   `CurrencyAPIError`: For issues related to API communication (network errors, HTTP errors, JSON parsing failures).
    -   `CurrencyNotFoundError`: When a currency definition or its specific data isn't found.
-   Uses Python's `logging` module for informative output and error reporting.
-   Allows configuration of currency item IDs and the API base URL for flexibility.
-   Packaged using `pyproject.toml` with Hatchling as the build backend.
-   Comes with a comprehensive unit test suite using `pytest`, `pytest-asyncio`, and `respx` (for mocking `httpx` calls).
-   Includes helper scripts for environment setup and running a demo.

## Installation

### From PyPI (Recommended for users)

Once the package is published to PyPI, you can install it using pip:

```bash
pip install tgju
```
*(Note: At the time of writing this README, the package might not yet be on PyPI.)*

### From Source (For development)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ahmoloudi/tgju.git # Replace with your repo URL if forked
    cd tgju
    ```
2.  **Create and activate a virtual environment** (recommended):
    *   Linux/macOS:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   Windows:
        ```bat
        python -m venv venv
        venv\Scripts\activate
        ```
3.  **Install in editable mode**:
    This installs the package and its core dependencies.
    ```bash
    pip install -e .
    ```
4.  **To include test and development dependencies**:
    ```bash
    pip install -e ".[test]"
    ```
    Alternatively, the provided `setup.sh` (for Linux/macOS) or `setup.bat` (for Windows) scripts can be used to create a virtual environment and install dependencies from `requirements.txt`. These are primarily for convenience in a development setup.

## Usage

### As a Module (Library Usage)

The primary function `get_currency_price` is asynchronous and must be run within an asyncio event loop.

**Importing:**
```python
from tgju import get_currency_price, DEFAULT_CURRENCY_IDS, CurrencyError
```

**Function Signature:**
```python
async def get_currency_price(
    item_name_to_find: str,
    currency_ids: Dict[str, str],
    base_api_url: str = DEFAULT_API_BASE_URL  # from tgju module
) -> str:
```
-   `item_name_to_find` (str): The common name of the currency (must be a key in `currency_ids`).
-   `currency_ids` (Dict[str, str]): A dictionary mapping currency names to their API item IDs.
-   `base_api_url` (str, optional): The base URL for the API. Defaults to `DEFAULT_API_BASE_URL` from the `tgju` module.

**Returns:**
-   `str`: The price of the currency as a string.

**Raises:**
-   `CurrencyNotFoundError`: If the currency name isn't in `currency_ids`, or if its data/price isn't in the API response.
-   `CurrencyAPIError`: For API communication issues (network, HTTP errors, JSON parsing).

**Example:**
```python
import asyncio
import logging
from tgju import (
    get_currency_price,
    DEFAULT_CURRENCY_IDS,
    CurrencyError, # Base exception for catching both API and Not Found errors
    __version__ as tgju_version
)

# Optional: Configure a basic logger for your application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def fetch_aed_price_example():
    logger.info(f"Using tgju package version: {tgju_version}")
    try:
        # Using default currency IDs and API URL from the tgju package
        aed_price = await get_currency_price("درهم امارات ", DEFAULT_CURRENCY_IDS)
        logger.info(f"Successfully fetched AED price: {aed_price}")
        return aed_price
    except CurrencyError as e: # Catches both CurrencyAPIError and CurrencyNotFoundError
        logger.error(f"Could not retrieve AED price: {e}")
        return None

if __name__ == "__main__":
    retrieved_price = asyncio.run(fetch_aed_price_example())
    if retrieved_price:
        print(f"Retrieved AED price via example: {retrieved_price}")
    else:
        print("Failed to retrieve AED price in example.")
```

### Running the Demo (Directly from Source)

The repository includes `run.sh` (for Linux/macOS) and `run.bat` (for Windows) to demonstrate the `currency_service.py` script. These scripts:
1.  Activate the virtual environment (if `venv` directory exists).
2.  Set `PYTHONPATH` to include the `src` directory.
3.  Execute `python -B src/tgju/currency_service.py`.

The demo script itself (`src/tgju/currency_service.py` when run as `__main__`) fetches the price for "درهم امارات " and logs the outcome.

*   **For Linux/macOS:**
    ```bash
    chmod +x run.sh
    ./run.sh
    ```
*   **For Windows:**
    ```bat
    run.bat
    ```
To run the demo script manually (ensure virtual environment is active and you are in the project root):
```bash
# For Linux/macOS
PYTHONPATH=./src:$PYTHONPATH python -B src/tgju/currency_service.py

# For Windows (cmd)
set "PYTHONPATH=.\src;%PYTHONPATH%"
python -B src\tgju\currency_service.py
```

## Configuration

The `tgju` package can be configured by providing parameters to the `get_currency_price` function. Default values are defined in `src/tgju/currency_service.py` and exposed via `src/tgju/__init__.py`:

-   `DEFAULT_CURRENCY_IDS: Dict[str, str]`: A dictionary mapping currency names to their TGJU API item IDs.
    ```python
    # from tgju import DEFAULT_CURRENCY_IDS
    # print(DEFAULT_CURRENCY_IDS)
    # Output: {"درهم امارات ": "137206"}
    ```
-   `DEFAULT_API_BASE_URL: str`: The base URL for the TGJU API endpoint.

To use custom configurations, pass your own `currency_ids` dictionary and/or `base_api_url` string to `get_currency_price`.

## Running Tests

Tests are located in the `tests/` directory and use the `pytest` framework, along with `pytest-asyncio` for asynchronous tests and `respx` for mocking HTTP requests.

To run the tests:

1.  **Ensure test dependencies are installed.** If you installed the package with `pip install -e ".[test]"`, they are already there. Otherwise, install them:
    ```bash
    pip install pytest pytest-asyncio respx
    ```
    (These are also listed in `requirements.txt`).
2.  **Navigate to the project root directory** (where `pyproject.toml` is located).
3.  **Run pytest:**
    ```bash
    pytest
    ```
    `pytest` will automatically discover and run tests from the `tests/` directory. It handles the `src` layout correctly due to `pyproject.toml` and Python path resolution.

## Building the Package

This project uses `pyproject.toml` and [Hatchling](https://hatch.pypa.io/latest/) as the build backend.

1.  **Ensure build tools are installed:**
    ```bash
    pip install build
    ```
    (`build` is also listed in `requirements.txt`).
2.  **From the project root directory, run the build command:**
    ```bash
    python -m build
    ```
This will generate a wheel (`.whl`) and a source distribution (`.tar.gz`) in the `dist/` directory. These are the files you would upload to PyPI.

## Contributing

Contributions are welcome! For development, it's recommended to set up the environment using `pip install -e ".[test]"` to get all dependencies. Please ensure tests pass with `pytest` before submitting pull requests.

Key tools used:
-   `httpx` for asynchronous HTTP requests.
-   `respx` for mocking HTTPX calls in tests.
-   `pytest` and `pytest-asyncio` for running tests.
-   `Hatchling` for building the package.
-   `logging` for application logs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
