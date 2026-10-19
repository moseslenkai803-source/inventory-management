import requests
import pytest

import openfoodfacts_service as service


def test_fetch_product_by_barcode(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "status": 1,
                "product": {
                    "code": "1234567890123",
                    "product_name": "Almond Milk",
                    "categories": "Beverages",
                    "brands": "Example Brand",
                    "ingredients_text": "Water, almonds",
                    "image_url": "https://example.com/image.jpg",
                },
            }

    def mock_get(url, **kwargs):
        assert "1234567890123" in url
        return MockResponse()

    monkeypatch.setattr(service.requests, "get", mock_get)

    product = service.fetch_product_by_barcode("1234567890123")

    assert product["barcode"] == "1234567890123"
    assert product["name"] == "Almond Milk"
    assert product["category"] == "Beverages"
    assert product["source"] == "openfoodfacts"


def test_fetch_product_by_barcode_returns_none_when_missing(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"status": 0, "product": None}

    monkeypatch.setattr(
        service.requests,
        "get",
        lambda *args, **kwargs: MockResponse(),
    )

    assert service.fetch_product_by_barcode("0000000000000") is None


def test_fetch_product_by_barcode_handles_request_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.ConnectionError("Connection failed")

    monkeypatch.setattr(service.requests, "get", mock_get)

    with pytest.raises(service.OpenFoodFactsError):
        service.fetch_product_by_barcode("1234567890123")


def test_search_products_by_name(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "products": [
                    {
                        "code": "123",
                        "product_name": "Almond Milk",
                        "brands": "Example Brand",
                    },
                    {
                        "code": "456",
                        "product_name": "Unsweetened Almond Milk",
                    },
                    {"code": "789"},
                ]
            }

    def mock_get(url, **kwargs):
        assert "search.pl" in url
        assert kwargs["params"]["search_terms"] == "almond milk"
        return MockResponse()

    monkeypatch.setattr(service.requests, "get", mock_get)

    products = service.search_products_by_name(" almond milk ")

    assert len(products) == 2
    assert products[0]["name"] == "Almond Milk"
    assert products[1]["name"] == "Unsweetened Almond Milk"


def test_search_products_by_name_returns_empty_for_blank_name():
    assert service.search_products_by_name("  ") == []


def test_search_products_handles_request_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.Timeout("Request timed out")

    monkeypatch.setattr(service.requests, "get", mock_get)

    with pytest.raises(service.OpenFoodFactsError):
        service.search_products_by_name("almond milk")
