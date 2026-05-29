from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.connection import engine
from database.models import Base, Product
from database.db import get_db

app=FastAPI()

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
