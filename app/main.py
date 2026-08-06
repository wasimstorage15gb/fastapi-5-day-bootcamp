from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


# Main FastAPI application object
app = FastAPI(
    title="Wasim Product API",
    description="Day 1 project for learning FastAPI and REST API fundamentals",
    version="1.0.0",
)


# Request model:
# Client product create karte waqt ye fields bhejega.
class ProductCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
        examples=["Laptop"],
    )
    price: float = Field(
        gt=0,
        examples=[2500],
    )
    quantity: int = Field(
        ge=0,
        examples=[5],
    )
    category: str | None = Field(
        default=None,
        max_length=50,
        examples=["Electronics"],
    )


# Response model:
# ProductCreate ke saare fields + server-generated ID.
class Product(ProductCreate):
    id: int


# Temporary in-memory data.
# Server restart hone par newly created products disappear ho jayenge.
products: list[Product] = [
    Product(
        id=1,
        name="Laptop",
        price=2500,
        quantity=5,
        category="Electronics",
    ),
    Product(
        id=2,
        name="Keyboard",
        price=150,
        quantity=20,
        category="Accessories",
    ),
]


@app.get(
    "/",
    tags=["General"],
)
def home():
    """Return basic information about the API."""

    return {
        "message": "Wasim Product API is running",
        "documentation": "/docs",
        "version": "1.0.0",
    }


@app.get(
    "/health",
    tags=["General"],
)
def health_check():
    """Check whether the API is running."""

    return {
        "status": "healthy",
    }


@app.get(
    "/products",
    response_model=list[Product],
    tags=["Products"],
)
def get_products(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of products to return",
    ),
    category: str | None = Query(
        default=None,
        description="Filter products by category",
    ),
):
    """Return products with optional limit and category filters."""

    filtered_products = products

    if category:
        filtered_products = [
            product
            for product in products
            if product.category
            and product.category.lower() == category.lower()
        ]

    return filtered_products[:limit]


@app.get(
    "/products/{product_id}",
    response_model=Product,
    tags=["Products"],
)
def get_product(product_id: int):
    """Return one product using its ID."""

    for product in products:
        if product.id == product_id:
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with ID {product_id} was not found",
    )


@app.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
)
def create_product(product_data: ProductCreate):
    """Create a new product."""

    next_product_id = max(
        (product.id for product in products),
        default=0,
    ) + 1

    new_product = Product(
        id=next_product_id,
        **product_data.model_dump(),
    )

    products.append(new_product)

    return new_product