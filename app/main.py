from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="Wasim Product API",
    description=(
        "FastAPI five-day bootcamp project covering CRUD operations, "
        "validation, filtering and error handling."
    ),
    version="2.0.0",
)


# ---------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------


class ProductBase(BaseModel):
    """Fields shared by product creation and product response models."""

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


class ProductCreate(ProductBase):
    """Request model used while creating or fully replacing a product."""

    pass


class Product(ProductBase):
    """Complete product returned by the API."""

    id: int


class ProductPatch(BaseModel):
    """
    Partial-update model.

    Every field is optional because the client may update only one field.
    """

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
        examples=["Gaming Laptop"],
    )
    price: float | None = Field(
        default=None,
        gt=0,
        examples=[3200],
    )
    quantity: int | None = Field(
        default=None,
        ge=0,
        examples=[3],
    )
    category: str | None = Field(
        default=None,
        max_length=50,
        examples=["Computers"],
    )


# ---------------------------------------------------------
# Temporary in-memory database
# ---------------------------------------------------------


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
    Product(
        id=3,
        name="Office Chair",
        price=450,
        quantity=8,
        category="Furniture",
    ),
]


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------


def find_product_index(product_id: int) -> int:
    """
    Find the position of a product in the list.

    Raise 404 when the product does not exist.
    """

    for index, product in enumerate(products):
        if product.id == product_id:
            return index

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with ID {product_id} was not found",
    )


def ensure_unique_product_name(
    name: str,
    ignore_product_id: int | None = None,
) -> None:
    """
    Prevent two products from using the same name.

    ignore_product_id is used while updating an existing product.
    """

    for product in products:
        same_name = product.name.casefold() == name.casefold()
        different_product = product.id != ignore_product_id

        if same_name and different_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A product named '{name}' already exists",
            )


# ---------------------------------------------------------
# General endpoints
# ---------------------------------------------------------


@app.get(
    "/",
    tags=["General"],
    summary="Get API information",
)
def home():
    """Return basic API information."""

    return {
        "message": "Wasim Product API is running",
        "version": "2.0.0",
        "documentation": "/docs",
        "features": [
            "Create products",
            "Read products",
            "Update products",
            "Delete products",
            "Search and filter products",
        ],
    }


@app.get(
    "/health",
    tags=["General"],
    summary="Check API health",
)
def health_check():
    """Return the current API health status."""

    return {
        "status": "healthy",
        "version": "2.0.0",
    }


# ---------------------------------------------------------
# Read endpoints
# ---------------------------------------------------------


@app.get(
    "/products",
    response_model=list[Product],
    tags=["Products"],
    summary="List and filter products",
)
def get_products(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of products to return",
    ),
    search: str | None = Query(
        default=None,
        min_length=1,
        description="Search within product names",
    ),
    category: str | None = Query(
        default=None,
        min_length=1,
        description="Filter products by category",
    ),
    min_price: float | None = Query(
        default=None,
        ge=0,
        description="Minimum product price",
    ),
    max_price: float | None = Query(
        default=None,
        ge=0,
        description="Maximum product price",
    ),
):
    """Return products using optional search and filter parameters."""

    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price cannot be greater than max_price",
        )

    filtered_products = products

    if search:
        filtered_products = [
            product
            for product in filtered_products
            if search.casefold() in product.name.casefold()
        ]

    if category:
        filtered_products = [
            product
            for product in filtered_products
            if product.category
            and product.category.casefold() == category.casefold()
        ]

    if min_price is not None:
        filtered_products = [
            product
            for product in filtered_products
            if product.price >= min_price
        ]

    if max_price is not None:
        filtered_products = [
            product
            for product in filtered_products
            if product.price <= max_price
        ]

    return filtered_products[:limit]


@app.get(
    "/products/{product_id}",
    response_model=Product,
    tags=["Products"],
    summary="Get one product",
)
def get_product(product_id: int):
    """Return a product using its ID."""

    product_index = find_product_index(product_id)

    return products[product_index]


# ---------------------------------------------------------
# Create endpoint
# ---------------------------------------------------------


@app.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
    summary="Create a product",
)
def create_product(product_data: ProductCreate):
    """Create a new product after validating its name and fields."""

    ensure_unique_product_name(product_data.name)

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


# ---------------------------------------------------------
# Full update endpoint
# ---------------------------------------------------------


@app.put(
    "/products/{product_id}",
    response_model=Product,
    tags=["Products"],
    summary="Fully replace a product",
)
def replace_product(
    product_id: int,
    product_data: ProductCreate,
):
    """
    Completely replace an existing product.

    All required product fields must be supplied.
    """

    product_index = find_product_index(product_id)

    ensure_unique_product_name(
        product_data.name,
        ignore_product_id=product_id,
    )

    replacement_product = Product(
        id=product_id,
        **product_data.model_dump(),
    )

    products[product_index] = replacement_product

    return replacement_product


# ---------------------------------------------------------
# Partial update endpoint
# ---------------------------------------------------------


@app.patch(
    "/products/{product_id}",
    response_model=Product,
    tags=["Products"],
    summary="Partially update a product",
)
def update_product(
    product_id: int,
    product_data: ProductPatch,
):
    """
    Update only the product fields supplied by the client.
    """

    product_index = find_product_index(product_id)

    update_data = product_data.model_dump(
        exclude_unset=True,
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one field to update",
        )

    required_fields = ("name", "price", "quantity")

    for field_name in required_fields:
        if (
            field_name in update_data
            and update_data[field_name] is None
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"{field_name} cannot be null",
            )

    if "name" in update_data:
        ensure_unique_product_name(
            update_data["name"],
            ignore_product_id=product_id,
        )

    stored_product = products[product_index]

    updated_product = stored_product.model_copy(
        update=update_data,
    )

    products[product_index] = updated_product

    return updated_product


# ---------------------------------------------------------
# Delete endpoint
# ---------------------------------------------------------


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Products"],
    summary="Delete a product",
)
def delete_product(product_id: int) -> Response:
    """Delete an existing product."""

    product_index = find_product_index(product_id)

    products.pop(product_index)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )