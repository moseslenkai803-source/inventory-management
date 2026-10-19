import pytest
import inventory as inventory_data
from app import app


@pytest.fixture(autouse=True)
def reset_inventory():
    inventory_data.inventory.clear()
    inventory_data.inventory.extend([
        {
            "id": 1,
            "name": "Organic Almond Milk",
            "barcode": "1234567890123",
            "category": "Beverages",
            "quantity": 20,
            "price": 350.00,
            "brand": "Silk",
            "ingredients": "Filtered water, almonds, cane sugar",
            "image_url": None,
            "source": "mock"
        },
        {
            "id": 2,
            "name": "Wholegrain Cereal",
            "barcode": "2345678901234",
            "category": "Breakfast",
            "quantity": 15,
            "price": 450.00,
            "brand": "Example Foods",
            "ingredients": None,
            "image_url": None,
            "source": "mock"
        }
    ])
    inventory_data.next_id = 3


def test_get_inventory_returns_all_items():
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/inventory")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Organic Almond Milk"
    assert data[1]["name"] == "Wholegrain Cereal"

def test_get_inventory_item_returns_matching_item():
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/inventory/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["name"] == "Organic Almond Milk"

def test_get_inventory_item_returns_404_when_item_not_found():
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/inventory/999")

    assert response.status_code == 404

    data = response.get_json()

    assert "error" in data
    assert data["error"] == "Item not found"


def test_create_inventory_item():
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.post(
        "/inventory",
        json={
            "name": "Rice",
            "category": "Grains",
            "quantity": 10,
            "price": 250
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "Rice"
    assert data["id"] == 3

def test_create_inventory_item_missing_required_field():
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.post(
        "/inventory",
        json={
            "name": "Rice",
            "quantity": 10,
            "price": 250
        }
    )

    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Missing required field: category"

def test_update_inventory_item():
    client = app.test_client()

    response = client.patch(
        "/inventory/1",
        json={"quantity": 12}
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["quantity"] == 12
    assert data["name"] == "Organic Almond Milk"
    assert data["price"] == 350.00

def test_update_inventory_item_not_found():
    client = app.test_client()

    response = client.patch(
        "/inventory/999",
        json={"quantity": 12}
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Item not found"

def test_update_inventory_item_rejects_unknown_field():
    client = app.test_client()

    response = client.patch(
        "/inventory/1",
        json={"quanity": 12}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Unknown field"


def test_delete_inventory_item():
    response = app.test_client().delete("/inventory/1")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Item deleted successfully"
    }
    assert not any(item["id"] == 1 for item in inventory_data.inventory)


def test_delete_inventory_item_not_found():
    response = app.test_client().delete("/inventory/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Item not found"}


def test_create_inventory_item_rejects_negative_quantity():
    client = app.test_client()

    response = client.post(
        "/inventory",
        json={
            "name": "Rice",
            "category": "Grains",
            "quantity": -5,
            "price": 250
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Quantity must be non-negative"


def test_create_inventory_item_rejects_negative_price():
    client = app.test_client()

    response = client.post(
        "/inventory",
        json={
            "name": "Rice",
            "category": "Grains",
            "quantity": 10,
            "price": -250
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Price must be non-negative"


def test_create_inventory_item_rejects_client_supplied_id():
    client = app.test_client()

    response = client.post(
        "/inventory",
        json={
            "id": 99,
            "name": "Rice",
            "category": "Grains",
            "quantity": 10,
            "price": 250
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Do not provide an ID"

def test_create_inventory_item_rejects_non_integer_quantity():
    client = app.test_client()

    response = client.post(
        "/inventory",
        json={
            "name": "Rice",
            "category": "Grains",
            "quantity": "ten",
            "price": 250
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Quantity must be non-negative"


def test_create_inventory_item_rejects_non_numeric_price():
    client = app.test_client()

    response = client.post(
        "/inventory",
        json={
            "name": "Rice",
            "category": "Grains",
            "quantity": 10,
            "price": "cheap"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Price must be non-negative"


def test_update_inventory_item_rejects_negative_quantity():
    client = app.test_client()

    response = client.patch(
        "/inventory/1",
        json={"quantity": -5}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Quantity must be non-negative"


def test_update_inventory_item_rejects_negative_price():
    client = app.test_client()

    response = client.patch(
        "/inventory/1",
        json={"price": -100}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Price must be non-negative"
