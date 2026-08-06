
# FastAPI Day 2 Cheatsheet

## Run API

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

## CRUD Methods

```text
POST   = Create
GET    = Read
PUT    = Full update
PATCH  = Partial update
DELETE = Delete
```

## Full Update

```python
@app.put("/products/{product_id}")
def replace_product(
    product_id: int,
    product_data: ProductCreate,
):
    ...
```

PUT normally expects every required field.

## Partial Update Model

```python
class ProductPatch(BaseModel):
    name: str | None = None
    price: float | None = None
    quantity: int | None = None
    category: str | None = None
```

## Only Supplied Fields

```python
update_data = product_data.model_dump(
    exclude_unset=True,
)
```

## Copy Model With Updates

```python
updated_product = stored_product.model_copy(
    update=update_data,
)
```

## Delete Resource

```python
@app.delete(
    "/products/{product_id}",
    status_code=204,
)
def delete_product(product_id: int):
    ...
```

## Important Status Codes

```text
200 = Successful read or update
201 = Resource created
204 = Deleted, no response body
400 = Invalid logical request
404 = Resource not found
409 = Duplicate/conflict
422 = Validation failure
500 = Server error
```

## Duplicate Check

```python
if existing_product:
    raise HTTPException(
        status_code=409,
        detail="Product already exists",
    )
```

## Search Query

```text
GET /products?search=laptop
```

## Price Filter

```text
GET /products?min_price=100&max_price=1000
```

## Daily Git Workflow

```powershell
git status
git diff
git add .
git commit -m "meaningful message"
git push
```

## Feature Branch Workflow

```powershell
git switch main
git pull
git switch -c feature-name

# Make changes

git add .
git commit -m "describe change"
git push -u origin feature-name
```
