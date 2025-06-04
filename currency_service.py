import requests
from json.decoder import JSONDecodeError

CURRENCY_IDS = {"درهم امارات ": "137206"}

def get_currency_price(item_name_to_find: str) -> str | None:
    """
    Retrieves the price of a currency from the tgju.org API.

    Args:
        item_name_to_find: The name of the currency to find.

    Returns:
        The price of the currency as a string, or None if an error occurs.
    """
    if item_name_to_find not in CURRENCY_IDS:
        print(f"Error: Currency '{item_name_to_find}' not found in CURRENCY_IDS.")
        return None

    item_id = CURRENCY_IDS[item_name_to_find]
    api_url = f"https://api.tgju.org/v1/widget/tmp?keys={item_id}"

    try:
        response = requests.get(api_url)
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed: {e}")
        return None

    if response.status_code != 200:
        print(f"Error: API request failed with status code {response.status_code}: {response.text}")
        return None

    try:
        data = response.json()
    except JSONDecodeError as e:
        print(f"Error: Failed to parse JSON response: {e}")
        return None

    indicators = data.get("response", {}).get("indicators", [])

    for indicator_data in indicators:
        if str(indicator_data.get("item_id")) == item_id:
            return indicator_data.get("p")

    print(f"Error: Item ID '{item_id}' not found in API response.")
    return None

if __name__ == "__main__":
    aed_price = get_currency_price("درهم امارات ")
    if aed_price:
        print(f"The price of درهم امارات is: {aed_price}")
    else:
        print("Could not retrieve the price for درهم امارات.")

    # Test a non-existent currency
    fake_price = get_currency_price("خیالی")
    if fake_price:
        print(f"The price of خیالی is: {fake_price}")
    else:
        print("Could not retrieve the price for خیالی.")
