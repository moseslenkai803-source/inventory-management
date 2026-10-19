import requests

BASE_URL = "https://world.openfoodfacts.org"
HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0"
}
TIMEOUT = 10


class OpenFoodFactsError(Exception):
    """Raised when the external product service cannot be reached."""


def normalize_product(product):
    """Convert an OpenFoodFacts product into our inventory format."""
    return {
        "barcode": product.get("code") or product.get("_id"),
        "name": product.get("product_name") or "Unknown product",
        "category": product.get("categories") or "Uncategorized",
        "brand": product.get("brands"),
        "ingredients": product.get("ingredients_text"),
        "image_url": product.get("image_url"),
        "source": "openfoodfacts",
    }


def fetch_product_by_barcode(barcode):
    """Return one product matching a barcode, or None if not found."""
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise OpenFoodFactsError(
            "Unable to retrieve product from OpenFoodFacts"
        ) from exc

    if data.get("status") != 1 or not data.get("product"):
        return None

    return normalize_product(data["product"])


def search_products_by_name(name):
    """Return products matching a product name."""
    if not isinstance(name, str) or not name.strip():
        return []

    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": name.strip(),
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 10,
        "fields": (
            "code,product_name,categories,brands,"
            "ingredients_text,image_url"
        ),
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise OpenFoodFactsError(
            "Unable to search OpenFoodFacts"
        ) from exc

    products = data.get("products", [])

    return [
        normalize_product(product)
        for product in products
        if product.get("product_name")
    ]
