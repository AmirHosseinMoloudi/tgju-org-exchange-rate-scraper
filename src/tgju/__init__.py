# src/tgju/__init__.py
"""Python client for fetching live currency and asset prices from the TGJU API.

This package provides an asynchronous client to interact with the TGJU (unofficial) API
for retrieving various financial data points, primarily focusing on currency exchange rates.
"""

__version__ = "0.0.1b0"
__author__ = "AmirHosseinMoloudi <ahmoloudi786@gmail.com>"
__license__ = "MIT"

from .currency_service import (
    get_currency_price,
    CurrencyError,
    CurrencyAPIError,
    CurrencyNotFoundError,
    DEFAULT_CURRENCY_IDS,
    DEFAULT_API_BASE_URL
)

__all__ = [
    "get_currency_price",
    "CurrencyError",
    "CurrencyAPIError",
    "CurrencyNotFoundError",
    "DEFAULT_CURRENCY_IDS",
    "DEFAULT_API_BASE_URL",
    "__version__",
    "__author__",
    "__license__",
]
