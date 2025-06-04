# TGJU Currency Price Fetcher

This Python module, `currency_service.py`, fetches the live price of a specified currency from an external API provided by tgju.org. Currently, it's configured to retrieve the price for "درهم امارات " (AED).

## Features

-   Fetches live currency prices using the item ID.
-   Parses JSON responses from the API.
-   Includes error handling for various scenarios (API errors, JSON errors, item not found).
-   Comes with a set of unit tests.

## Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    # git clone <repository-url>
    # cd <repository-directory>
    ```

2.  **Automated Setup (Recommended):**
    *   **For Linux/macOS:**
        ```bash
        chmod +x setup.sh
        ./setup.sh
        ```
    *   **For Windows:**
        ```bat
        setup.bat
        ```
    These scripts will attempt to create a virtual environment in a directory named `venv` and install the required dependencies from `requirements.txt`.

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
        ```bash
        pip install -r requirements.txt
        ```

## Usage

Ensure your virtual environment is activated if you are not using the run scripts.
(`source venv/bin/activate` or `venv\Scripts\activate`)

### As a Module

You can import and use the `get_currency_price` function in your own Python scripts:

```python
from currency_service import get_currency_price

price = get_currency_price("درهم امارات ")
if price:
    print(f"The live price of درهم امارات is: {price}")
else:
    print("Could not retrieve the price.")
```

### Using Run Scripts (Demo)

These scripts will activate the virtual environment and run the demo.
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

To see a demonstration by running the `currency_service.py` script directly (ensure virtual environment is active):

```bash
python currency_service.py
```
This will print the current price of "درهم امارات " to the console, or an error message if it fails.

## Running Tests

Unit tests are located in `test_currency_service.py` and use Python's `unittest` module. To run the tests:

```bash
python -m unittest test_currency_service.py
```
Alternatively, you can use:
```bash
python -m unittest discover
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
