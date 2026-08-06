# FastAPI Day 1 Cheatsheet

## Start Work

```powershell
cd fastapi-5-day-bootcamp
.venv\Scripts\Activate.ps1
git pull

Run API
fastapi dev app/main.py
Swagger UI
http://127.0.0.1:8000/docs
HTTP Methods
Method	Meaning
GET	Read
POST	Create
PUT	Full update
PATCH	Partial update
DELETE	Delete
Important Status Codes
Code	Meaning
200	Successful
201	Created
404	Not found
422	Validation failed
500	Server error
Basic Route
@app.get("/health")
def health_check():
    return {"status": "healthy"}
Path Parameter
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"product_id": product_id}
Query Parameter
@app.get("/products")
def get_products(limit: int = 10):
    return {"limit": limit}
Request Model
class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
Validation
name: str = Field(min_length=2, max_length=100)
price: float = Field(gt=0)
quantity: int = Field(ge=0)
Optional Value
category: str | None = None
HTTP Error
raise HTTPException(
    status_code=404,
    detail="Product not found",
)
Daily Git Workflow
git status
git add .
git commit -m "describe the completed work"
git push

---

# Phase 18: Final Documentation Commit

Check:

```powershell
git status

Stage only documentation:

git add README.md docs

Commit:

git commit -m "docs: complete Day 1 documentation"

Push:

git push
