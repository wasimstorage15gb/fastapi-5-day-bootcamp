
# Day 2 — Complete Product CRUD API

## Date

August 6, 2026

## Objective

Extend the Day 1 Product API with complete CRUD operations, partial updates, advanced filters, duplicate validation and professional error handling.

## Concepts Learned

### CRUD

CRUD represents the four primary data operations:

* Create
* Read
* Update
* Delete

### PUT

PUT performs a complete replacement of an existing resource.

The client supplies all required product fields. The existing product ID remains unchanged.

### PATCH

PATCH performs a partial update.

The client sends only the fields that need to change. Existing fields that are not supplied remain unchanged.

### `exclude_unset=True`

`model_dump(exclude_unset=True)` creates a dictionary containing only fields explicitly supplied by the client.

### DELETE

DELETE removes a resource.

The API returns `204 No Content` after a successful deletion.

## Pydantic Models

The project now uses separate models for different responsibilities:

| Model           | Purpose                                   |
| --------------- | ----------------------------------------- |
| `ProductBase`   | Shared product fields                     |
| `ProductCreate` | Product creation and complete replacement |
| `ProductPatch`  | Partial product updates                   |
| `Product`       | Complete API response including ID        |

## Endpoints

| Method | Endpoint                 | Purpose                          |
| ------ | ------------------------ | -------------------------------- |
| GET    | `/products`              | List, search and filter products |
| GET    | `/products/{product_id}` | Retrieve one product             |
| POST   | `/products`              | Create a product                 |
| PUT    | `/products/{product_id}` | Fully replace a product          |
| PATCH  | `/products/{product_id}` | Partially update a product       |
| DELETE | `/products/{product_id}` | Delete a product                 |

## Query Parameters

The product-list endpoint supports:

* `limit`
* `search`
* `category`
* `min_price`
* `max_price`

Example:

```text
GET /products?search=lap&min_price=1000&max_price=5000
```

## Error Handling

| Status | Scenario                           |
| -----: | ---------------------------------- |
|    400 | Empty PATCH or invalid price range |
|    404 | Product ID does not exist          |
|    409 | Duplicate product name             |
|    422 | Request-body validation failure    |
|    204 | Product successfully deleted       |

## Test Results

* [x] Product search tested
* [x] Category filter tested
* [x] Price-range filter tested
* [x] Invalid price range returned 400
* [x] Product creation returned 201
* [x] Duplicate name returned 409
* [x] PUT full replacement tested
* [x] PUT missing field returned 422
* [x] PATCH single field tested
* [x] PATCH multiple fields tested
* [x] Empty PATCH returned 400
* [x] Required null field rejected
* [x] Product deletion returned 204
* [x] Deleted product returned 404

## Errors Faced

### Error

Add the exact error message here.

### Cause

Add the reason here.

### Solution

Add the commands or code change that fixed it.

## Important Learning

1. PUT and PATCH have different update responsibilities.
2. Separate Pydantic models make API validation clearer.
3. Helper functions reduce repeated lookup and duplicate-checking code.
4. HTTP status codes help clients understand the result of a request.
5. Each meaningful development stage should have its own Git commit.

## Current Limitation

Products are still stored in memory. Data is removed when the server restarts.

A permanent SQLite database will be added on Day 3.

## Status

Completed
