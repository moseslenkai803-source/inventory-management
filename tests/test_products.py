import app as app_module
from unittest.mock import patch

from app import OpenFoodFactsError


def test_barcode_product_found():
    product = {"barcode": "12345", "name": "Milk"}

    with patch("app.fetch_product_by_barcode", return_value=product):
        response = app_module.app.test_client().get("/products/barcode/12345")

    assert response.status_code == 200
    assert response.get_json() == product


def test_barcode_product_not_found():
    with patch("app.fetch_product_by_barcode", return_value=None):
        response = app_module.app.test_client().get("/products/barcode/99999")

    assert response.status_code == 404


def test_barcode_service_failure():
    with patch(
        "app.fetch_product_by_barcode",
        side_effect=OpenFoodFactsError("Service unavailable"),
    ):
        response = app_module.app.test_client().get("/products/barcode/12345")

    assert response.status_code == 502


def test_search_requires_name():
    response = app_module.app.test_client().get("/products/search")

    assert response.status_code == 400


def test_search_products_success():
    products = [{"barcode": "12345", "name": "Milk"}]

    with patch("app.search_products_by_name", return_value=products):
        response = app_module.app.test_client().get(
            "/products/search?name=milk"
        )

    assert response.status_code == 200
    assert response.get_json() == products


def test_search_service_failure():
    with patch(
        "app.search_products_by_name",
        side_effect=OpenFoodFactsError("Service unavailable"),
    ):
        response = app_module.app.test_client().get(
            "/products/search?name=milk"
        )

    assert response.status_code == 502
