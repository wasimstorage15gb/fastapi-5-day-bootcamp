# Day 1 — FastAPI and REST API Fundamentals

## Date

August 6, 2026

## Objective

Build and test a basic Product API while understanding the core concepts of REST, HTTP, FastAPI, Pydantic and Git.

## Concepts Learned

### API

An API allows two applications to communicate using defined requests and responses.

### REST API

A REST API represents application data as resources and uses HTTP methods to perform actions on those resources.

### HTTP Methods

- GET: Read data
- POST: Create data
- PUT: Completely update data
- PATCH: Partially update data
- DELETE: Remove data

### Endpoint


An endpoint is a combination of an HTTP method and a URL path.

Example:

```text
GET /products


Path Parameter

Used to identify a specific resource.

GET /products/1
Query Parameter

Used for filtering or limiting results.

GET /products?limit=1
GET /products?category=Electronics
Request Body

JSON data sent by the client to the API.

{
  "name": "Monitor",
  "price": 800,
  "quantity": 4,
  "category": "Electronics"
}
Pydantic Validation

Pydantic validates the data type and business rules of incoming request data.

Validation rules used:

Name length: 2–100 characters
Price: Greater than zero
Quantity: Zero or greater
Category: Optional
Endpoints Created
Method	Endpoint	Result
GET	/	API details
GET	/health	Health status
GET	/products	Product list
GET	/products/{id}	Specific product
POST	/products	New product
Test Results
 Root endpoint tested
 Health endpoint tested
 Product list tested
 Limit query tested
 Category filter tested
 Existing product tested
 Missing product returned 404
 Valid product created
 Invalid name rejected
 Negative price rejected
 Negative quantity rejected
 Missing required field rejected
HTTP Status Codes Observed
200 OK
201 Created
404 Not Found
422 Unprocessable Content / Validation Error
Git Commands Practised
git clone
git status
git add
git commit
git push
git log --oneline
Error Log
Error 1

Error: Add the error you faced here.

Cause: Add the cause here.

Solution: Add the solution here.

Three Key Learnings
FastAPI uses decorators to connect HTTP methods and URL paths with Python functions.
Pydantic validates incoming JSON before the main function processes it.
Git commits should represent meaningful stages of project development.
Current Limitation

The project uses an in-memory Python list instead of a database.

Day 1 Status

Completed


Error nahi aaya toh Error Log mein likho:

```markdown
No major errors were encountered during the initial setup.
