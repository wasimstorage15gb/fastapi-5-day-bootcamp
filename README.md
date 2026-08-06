# FastAPI 5-Day Bootcamp

A hands-on FastAPI learning project focused on building, testing and documenting practical REST APIs.

## Objective

The goal of this bootcamp is to learn FastAPI through practical development without repeating the complete Python syllabus.

Python concepts are revised only when they are required for API development.

## Progress

- [x] Day 1: REST API fundamentals, GET/POST routes and validation
- [x] Day 2: Complete CRUD, PUT, PATCH, DELETE and filtering
- [ ] Day 3: SQLite database integration
- [ ] Day 4: User authentication and JWT
- [ ] Day 5: Production structure, testing and final project

## Day 1 Features

- FastAPI application setup
- Automatic Swagger documentation
- Health-check endpoint
- Product listing
- Product lookup by ID
- Query parameter filtering
- Product creation
- Pydantic request validation
- Response models
- HTTP status codes
- Error handling

## Project Structure

```text
fastapi-5-day-bootcamp/
├── app/
│   ├── __init__.py
│   └── main.py
├── docs/
│   ├── day-01.md
│   └── cheatsheets/
│       └── day-01-cheatsheet.md
├── .gitignore
├── README.md
└── requirements.txt

Setup

Clone the repository:

git clone YOUR_REPOSITORY_URL
cd fastapi-5-day-bootcamp

Create a virtual environment:

py -m venv .venv

Activate it in Windows PowerShell:

.venv\Scripts\Activate.ps1

Install the dependencies:

python -m pip install -r requirements.txt

Run the application:

fastapi dev app/main.py

Open Swagger UI:

http://127.0.0.1:8000/docs
Day 1 Endpoints
Method	Endpoint	Purpose
GET	/	API information
GET	/health	API health check
GET	/products	List products
GET	/products/{product_id}	Get one product
POST	/products	Create product
Query Examples

Limit results:

GET /products?limit=1

Filter by category:

GET /products?category=Electronics
Example Product Request
{
  "name": "Monitor",
  "price": 800,
  "quantity": 4,
  "category": "Electronics"
}
Current Limitation

Products are stored in memory. Newly created products disappear when the application restarts.

Database integration will be added on Day 3.

Documentation
Day 1 Notes
Day 1 Cheatsheet
Author

Wasim Akram Khan

Learning Cloud, Cybersecurity, AI Engineering and secure application development.


Replace:

```text
YOUR_REPOSITORY_URL

with actual repository URL.
