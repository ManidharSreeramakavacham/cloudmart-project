from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

# Temporary database
inventory = []

# Product Structure
class Product(BaseModel):
    name: str
    quantity: int
    price: float

@app.get("/")
def home():
    return {"message":"CloudMart ERP Online"}

# View Inventory
@app.get("/products")
def get_inventory():
    return inventory

# Add Product
@app.post("/products")
def add_product(product: Product):
    inventory.append(product.dict())
    return {"message": "Product added successfully", 
            "product": product
        }   