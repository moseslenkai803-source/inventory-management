# Inventory Management System

## 1. Project Overview

The Inventory Management System is a Python application for managing inventory records through a REST API, a browser-based administration interface, and a command-line interface (CLI).

The system also integrates with the OpenFoodFacts API to retrieve food product information by barcode or product name.

This project is being developed as part of the **Summative Lab: Python REST API with Flask — Inventory Management System**.

### The problem this project solves

Businesses need a practical way to keep track of products, quantities, categories, and prices. Managing these records manually can lead to inconsistent information and errors.

This application provides a central interface for creating, viewing, updating, and deleting inventory records. External product lookup also helps users retrieve product information without entering every detail manually.

### Project objectives

- Build a REST API using Flask.
- Implement Create, Read, Update, and Delete (CRUD) operations.
- Validate incoming data and return appropriate HTTP status codes.
- Integrate with the OpenFoodFacts external API.
- Provide a command-line interface for inventory operations.
- Build a browser-based administration interface.
- Write automated tests for API routes and external-service behavior.
- Maintain a clear, testable project structure that can be extended with persistent storage.

---

## 2. Current Implementation Status

The following functionality has been implemented and checked.

| Component | Current status |
|---|---|
| Flask application | Implemented |
| Inventory CRUD API | Implemented |
| Request validation and error handling | Implemented |
| OpenFoodFacts barcode lookup | Implemented |
| OpenFoodFacts product search | Implemented |
| Command-line interface | Implemented |
| Browser-based administration interface | Implemented |
| Automated tests | Implemented |
| Python syntax checks | Passing |
| JavaScript syntax check | Passing |
| Automated test suite | 29 tests passing |
| Persistent database | Not implemented yet |
| Production deployment | Not configured yet |

This table describes the current implementation, not a claim that every possible production requirement has been completed.

---

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Flask | Web framework and REST API |
| Requests | HTTP communication with OpenFoodFacts |
| HTML | Web interface structure |
| CSS | Web interface styling |
| JavaScript | Browser-side API requests and interactions |
| pytest | Automated testing |
| OpenFoodFacts | External food product information |

### Why Flask?

Flask provides routing, request handling, and JSON responses without requiring a large framework. This makes it suitable for learning REST API design and organizing application logic.

### Why OpenFoodFacts?

OpenFoodFacts provides food product information that can be retrieved using a product barcode or a search term. The application uses this information to support product discovery.

External product information is not the same as an inventory record. Finding a product does not automatically mean that it has been saved into the inventory.

---

## 4. Project Structure

```text
inventory-management/
├── app.py
├── inventory.py
├── cli.py
├── openfoodfacts_service.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── styles.css
└── tests/
    ├── test_inventory.py
    ├── test_openfoodfacts.py
    └── test_products.py
```

### Responsibilities of the files

#### `app.py`

The main Flask application.

Responsibilities include:
- Registering HTTP routes.
- Handling inventory requests.
- Validating submitted inventory data.
- Returning JSON responses and HTTP status codes.
- Serving the homepage.
- Exposing product lookup endpoints.
- Translating external-service errors into API responses.

#### `inventory.py`

Contains the current inventory data and related in-memory state, including the next inventory identifier.

The application currently stores records in memory rather than in a database.

#### `openfoodfacts_service.py`

Contains the integration with OpenFoodFacts.

Responsibilities include:
- Fetching a product by barcode.
- Searching products by name.
- Normalizing external product data into a consistent structure.
- Handling request failures and invalid external responses.

#### `cli.py`

Provides a text-based interface for interacting with the application.

The CLI sends HTTP requests to the running Flask server rather than independently maintaining a separate inventory.

#### `templates/index.html`

Defines the structure of the browser-based administration interface.

#### `static/styles.css`

Contains the visual styling and responsive layout for the web interface.

#### `static/app.js`

Implements browser-side functionality, including:
- Loading and displaying inventory records.
- Submitting new inventory items.
- Editing existing records.
- Deleting records.
- Searching OpenFoodFacts by name.
- Looking up products by barcode.

#### `tests/`

Contains automated tests for inventory routes, validation, the external product service, and product API endpoints.

---

## 5. Installation and Setup

### Prerequisites

- Python 3.10 or newer.
- `pip`.
- Git.
- Internet access for external product lookups.
- Node.js is useful for checking JavaScript syntax but is not required to run the Flask application.

### Step 1: Clone the repository

```bash
git clone https://github.com/moseslenkai803-source/inventory-management.git
cd inventory-management
```

If you have already cloned the repository, navigate to the existing directory instead.

### Step 2: Create a virtual environment

```bash
python3 -m venv .venv
```

### Step 3: Activate the virtual environment

On Linux:

```bash
source .venv/bin/activate
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Verify the installation

```bash
python -m py_compile app.py cli.py openfoodfacts_service.py
python -m pytest -q
```

The current verified test result is **29 passed**.

---

## 6. Running the Application

### Start the Flask server

From the project directory, with the virtual environment activated:

```bash
python app.py
```

The application should be available at:

http://127.0.0.1:5000

Keep the server running while using the browser interface, CLI, or API clients.

### Open the administration interface

Visit:

http://127.0.0.1:5000/

The interface provides inventory display and forms for inventory operations and product lookup.

### Run the command-line interface

Open a second terminal, navigate to the project directory, and activate the virtual environment.

Then run:

```bash
python cli.py
```

The CLI communicates with the Flask server at `http://127.0.0.1:5000`. Start the server before using the CLI.

### Stop the server

Press `Ctrl+C` in the terminal running Flask.

---

## 7. REST API Reference

The REST API exposes inventory operations and external product lookup.

Base URL for local development:

`http://127.0.0.1:5000`

### Inventory endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/inventory` | Retrieve all inventory records |
| GET | `/inventory/<item_id>` | Retrieve one inventory record |
| POST | `/inventory` | Create an inventory record |
| PATCH | `/inventory/<item_id>` | Update selected fields |
| DELETE | `/inventory/<item_id>` | Delete an inventory record |

### Product lookup endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/products/barcode/<barcode>` | Retrieve a product using its barcode |
| GET | `/products/search?name=<name>` | Search OpenFoodFacts by product name |

### Example: retrieve all inventory records

```bash
curl http://127.0.0.1:5000/inventory
```

### Example: retrieve a single record

```bash
curl http://127.0.0.1:5000/inventory/1
```

Replace `1` with the identifier of the record you want to retrieve.

### Example: create an inventory record

```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Milk",
    "category": "Dairy",
    "quantity": 10,
    "price": 120.0
  }'
```

A successful request creates a record and returns a JSON response.

The identifier is generated by the application; clients should not supply their own `id`.

### Example: update an inventory record

```bash
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 15}'
```

This example updates the quantity of item `1`. Use an existing item identifier.

### Example: delete an inventory record

```bash
curl -X DELETE http://127.0.0.1:5000/inventory/1
```

### Example: search for a product

```bash
curl --get \
  --data-urlencode "name=milk" \
  http://127.0.0.1:5000/products/search
```

### Example: look up a barcode

```bash
curl http://127.0.0.1:5000/products/barcode/5449000000996
```

The barcode is an example. A lookup can return no result if OpenFoodFacts does not contain that product.

---

## 8. HTTP Status Codes and Validation

The API uses HTTP status codes to communicate the result of a request.

| Status | Meaning in this project |
|---|---|
| `200 OK` | A request succeeded |
| `201 Created` | A resource was created, where used by the endpoint |
| `400 Bad Request` | Submitted data is invalid or a required search parameter is missing |
| `404 Not Found` | The requested inventory item or external product was not found |
| `500 Internal Server Error` | An unexpected server error occurred |
| `502 Bad Gateway` | The external product service could not be used successfully |

The inventory API validates submitted data. Current tests cover cases including:
- Missing required fields.
- Negative quantities.
- Negative prices.
- Non-integer quantities.
- Non-numeric prices.
- Client-supplied identifiers.
- Unknown update fields.
- Requests for records that do not exist.

The exact response body and status depend on the route and the failure condition.

---

## 9. Inventory Data Model

An inventory record currently uses these main fields:

| Field | Purpose |
|---|---|
| `id` | Application-generated identifier |
| `name` | Product name |
| `category` | Product category |
| `quantity` | Quantity in inventory |
| `price` | Price associated with the item |

Example record:

```json
{
  "id": 1,
  "name": "Milk",
  "category": "Dairy",
  "quantity": 10,
  "price": 120.0
}
```

The identifier is generated by the application. Quantity must be a valid non-negative integer, and price must be numeric and non-negative.

This is the current application-level model. When persistent storage is introduced, the model and validation rules should be reviewed together with the database schema.

---

## 10. OpenFoodFacts Integration

The application integrates with OpenFoodFacts to find product information.

### Lookup by barcode

The service sends a request to the OpenFoodFacts product endpoint and checks whether the product was found.

### Search by name

The service sends a search request and returns a normalized list of matching products.

### Normalized product information

The service can return fields such as:

- Barcode.
- Product name.
- Category.
- Brand.
- Ingredients.
- Image URL.
- Source identifier.

Some fields may be missing because the external database is community-maintained and product records vary in completeness.

### Error handling

The service handles HTTP request failures and invalid JSON responses. The Flask API converts service failures into a `502` response.

A product that is not found is handled separately from an external-service failure.

### External service limitations

- An internet connection is required.
- Product data may be incomplete or outdated.
- Search results depend on the external service.
- Requests may fail because of connectivity, rate limits, or service availability.
- Tests should mock external HTTP requests so the test suite does not depend on a live internet connection.

---

## 11. Testing Strategy

Run all tests with:

```bash
python -m pytest -v
```

Run a shorter summary with:

```bash
python -m pytest -q
```

### Test modules

#### `tests/test_inventory.py`

Covers inventory retrieval, creation, updates, deletion, validation, and missing records.

#### `tests/test_openfoodfacts.py`

Covers external product lookup, name search, missing products, blank search terms, and request failures.

#### `tests/test_products.py`

Covers Flask product routes, including successful responses, missing products, missing search parameters, and external-service failures.

### Additional quality checks

Compile the Python files:

```bash
python -m py_compile app.py cli.py openfoodfacts_service.py
```

Check browser JavaScript syntax if Node.js is installed:

```bash
node --check static/app.js
```

Check Git whitespace errors:

```bash
git diff --check
```

These checks complement the automated tests. They do not replace manual verification of the browser interface and CLI.

---

## 12. Current Limitations

The following limitations should be considered during future development.

### In-memory storage

Inventory records are currently stored in memory. Changes may be lost when the server restarts, and data is not shared across independent application processes.

**Planned improvement:** introduce persistent database storage, migrations, and tests that verify database-backed CRUD operations.

### No configured authentication

The current interface is an administration interface, but a production deployment would need authentication and authorization before allowing users to change inventory.

**Planned improvement:** add user authentication, role-based permissions, secure session handling, and appropriate access controls.

### No production deployment configuration

The project is currently set up for local development.

**Planned improvement:** configure production settings, environment variables, deployment procedures, logging, and operational monitoring.

### External product data is not inventory data

A product returned by OpenFoodFacts is external information. The application should explicitly support any workflow that turns this information into an inventory record rather than assuming that a lookup automatically saves it.

### Additional operational concerns

Future work should consider concurrent updates, database transactions, API documentation, pagination, stronger integration tests, accessibility, and security hardening.

---

## 13. Development Roadmap

This roadmap guides our work. Items are planned, not claimed as completed.

### Phase 1 — Core functionality

- [x] Implement Flask inventory CRUD endpoints.
- [x] Add inventory data validation.
- [x] Integrate OpenFoodFacts lookup by barcode and name.
- [x] Build the CLI.
- [x] Build the browser interface.
- [x] Add automated tests for inventory and product routes.
- [x] Verify Python syntax and JavaScript syntax.
- [ ] Verify all browser interactions manually.
- [ ] Verify the complete CLI workflow against a running server.

### Phase 2 — Reliability and documentation

- [x] Document setup and current functionality.
- [x] Document API endpoints and examples.
- [ ] Review every requirement in the summative lab rubric.
- [ ] Confirm all required files are committed to Git.
- [ ] Push the final submission to GitHub.

### Phase 3 — Persistent data

- [ ] Select and configure a database.
- [ ] Design the inventory schema.
- [ ] Add database models and migrations.
- [ ] Replace in-memory storage with database-backed repositories.
- [ ] Add tests for persistence and failure cases.

### Phase 4 — Administration and security

- [ ] Add authentication and authorization.
- [ ] Improve user-facing error messages and loading states.
- [ ] Add audit information for inventory changes.
- [ ] Add API documentation and security checks.

### Phase 5 — Deployment and maintenance

- [ ] Configure production environment variables.
- [ ] Add structured logging and operational checks.
- [ ] Deploy to a suitable hosting environment.
- [ ] Document backup, recovery, and maintenance procedures.

---

## 14. Git Workflow

Check the working tree:

```bash
git status
```

Review changes before staging:

```bash
git diff --check
git diff
```

Stage the project files:

```bash
git add README.md app.py cli.py inventory.py openfoodfacts_service.py \
  requirements.txt templates static tests
```

Review what will be committed:

```bash
git status
git diff --cached --check
git diff --cached --stat
```

Commit only after reviewing the staged changes:

```bash
git commit -m "Complete inventory management system"
```

Push the commit:

```bash
git push origin main
```

If Git reports conflicts or the remote branch has new commits, stop and inspect the repository state before proceeding.

---

## 15. Definition of Done

Before considering the summative lab ready for submission, verify that:

- [ ] All rubric requirements are accounted for.
- [ ] Inventory CRUD works through the REST API.
- [ ] Validation and error responses behave correctly.
- [ ] OpenFoodFacts lookup works and handles failures.
- [ ] The CLI works against the running server.
- [ ] The browser interface supports its advertised operations.
- [ ] The automated test suite passes.
- [ ] Setup instructions work from a fresh clone.
- [ ] README instructions accurately describe the current implementation.
- [ ] Git contains the intended project files.
- [ ] The final commit is pushed to GitHub.

**Current verified baseline:** 29 automated tests pass, Python compilation passes, JavaScript syntax validation passes, and `git diff --check` reports no whitespace errors. Continue from this baseline and rerun the checks after changes.
