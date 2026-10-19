import requests

API_URL = "http://127.0.0.1:5000"


def display_response(response):
    try:
        data = response.json()
    except ValueError:
        print("Server returned an invalid response.")
        return

    print(f"\nHTTP {response.status_code}")
    print(data)


def list_inventory():
    response = requests.get(f"{API_URL}/inventory", timeout=10)
    display_response(response)


def view_inventory_item():
    item_id = input("Enter item ID: ").strip()
    response = requests.get(
        f"{API_URL}/inventory/{item_id}",
        timeout=10,
    )
    display_response(response)


def add_inventory_item():
    name = input("Product name: ").strip()
    category = input("Category: ").strip()

    try:
        quantity = int(input("Quantity: "))
        price = float(input("Price: "))
    except ValueError:
        print("Quantity must be an integer and price must be numeric.")
        return

    payload = {
        "name": name,
        "category": category,
        "quantity": quantity,
        "price": price,
    }

    response = requests.post(
        f"{API_URL}/inventory",
        json=payload,
        timeout=10,
    )
    display_response(response)


def update_inventory_item():
    item_id = input("Enter item ID: ").strip()
    field = input("Field to update (name, category, quantity, price): ").strip()

    if field not in {"name", "category", "quantity", "price"}:
        print("Unsupported field.")
        return

    value = input(f"New {field}: ").strip()

    try:
        if field == "quantity":
            value = int(value)
        elif field == "price":
            value = float(value)
    except ValueError:
        print("Quantity must be an integer and price must be numeric.")
        return

    response = requests.patch(
        f"{API_URL}/inventory/{item_id}",
        json={field: value},
        timeout=10,
    )
    display_response(response)


def delete_inventory_item():
    item_id = input("Enter item ID to delete: ").strip()
    confirm = input(f"Delete item {item_id}? (y/n): ").strip().lower()

    if confirm != "y":
        print("Deletion cancelled.")
        return

    response = requests.delete(
        f"{API_URL}/inventory/{item_id}",
        timeout=10,
    )
    display_response(response)


def search_openfoodfacts():
    name = input("Product name to search: ").strip()
    response = requests.get(
        f"{API_URL}/products/search",
        params={"name": name},
        timeout=15,
    )
    display_response(response)


def lookup_barcode():
    barcode = input("Product barcode: ").strip()
    response = requests.get(
        f"{API_URL}/products/barcode/{barcode}",
        timeout=15,
    )
    display_response(response)


def main():
    actions = {
        "1": list_inventory,
        "2": view_inventory_item,
        "3": add_inventory_item,
        "4": update_inventory_item,
        "5": delete_inventory_item,
        "6": search_openfoodfacts,
        "7": lookup_barcode,
    }

    while True:
        print(
            "\n=== Inventory Management ===\n"
            "1. List inventory\n"
            "2. View inventory item\n"
            "3. Add inventory item\n"
            "4. Update inventory item\n"
            "5. Delete inventory item\n"
            "6. Search OpenFoodFacts by name\n"
            "7. Look up OpenFoodFacts by barcode\n"
            "0. Exit"
        )

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye.")
            break

        action = actions.get(choice)

        if action is None:
            print("Invalid option. Choose 0–7.")
            continue

        try:
            action()
        except requests.RequestException as exc:
            print(f"Could not contact the Flask API: {exc}")


if __name__ == "__main__":
    main()
