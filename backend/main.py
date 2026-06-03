from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from database.connection import engine
from database.models import Base, Product
from database.db import get_db

app=FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create tables automatically
Base.metadata.create_all(bind=engine)

# Request model
class ProductCreate(BaseModel):
    name: str
    quantity: int
    price: float

# Home route
@app.get("/")
def home():
    return {"message": "CloudMart ERP Online"}

# Get All Products
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product

@app.get("/products/{product_id}")
def update_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Update product details
    product.name = updated_product.name
    product.quantity = updated_product.quantity
    product.price = updated_product.price

    db.commit()
    db.refresh(product)

    return {
        "message": "Product updated successfully", "product": {
            "id": product.id,
            "name": product.name,
            "quantity": product.quantity,
            "price": product.price
        }
    }

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }

# Add Product
@app.post("/products")
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
    ):
    
    new_product = Product(
        name=product.name,
        quantity=product.quantity,
        price=product.price
    )
    db.add(new_product)
    
    db.commit()
    
    db.refresh(new_product)
    
    return {
        "message": "Product added successfully", "product": {
            "id": new_product.id,
            "name": new_product.name,
            "quantity": new_product.quantity,
            "price": new_product.price
        }
    }
