# CloudMart ERP + AWS Learning Project

## Session Documentation — Backend & Database Foundations

### Duration: ~1.5 Hours

---

# 1. Mission Objective

Build a production-style ERP platform for fruits and vegetable vendors while learning:

* Backend Development
* Frontend Development
* Database Engineering
* AWS Cloud Infrastructure
* DevOps
* Enterprise Architecture

Future integration target:

* DCIM (Data Center Infrastructure Management)

---

# 2. Technologies Used

## Backend Framework

FastAPI

## Database

PostgreSQL

## ORM

SQLAlchemy

## PostgreSQL Driver

psycopg2

## API Documentation

Swagger UI (Automatically provided by FastAPI)

---

# 3. Project Structure

Final backend structure:

```text id="doc001"
cloudmart-project/
│
└── backend/
    │
    ├── database/
    │   ├── __init__.py
    │   ├── connection.py
    │   └── models.py
    │
    ├── venv/
    │
    ├── main.py
    ├── create_tables.py
    └── test_connection.py
```

---

# 4. Virtual Environment Setup

## Create Virtual Environment

```bash id="doc002"
python -m venv venv
```

---

## Activate Virtual Environment

### Windows CMD

```bash id="doc003"
venv\Scripts\activate
```

Expected terminal output:

```text id="doc004"
(venv)
```

---

# 5. FastAPI Installation

## Install Required Packages

```bash id="doc005"
pip install fastapi uvicorn
```

---

# 6. First Backend API

## Initial `main.py`

```python id="doc006"
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "CloudMart ERP Online"}
```

---

# 7. Running Backend Server

## Start Server

```bash id="doc007"
uvicorn main:app --reload
```

Expected:

```text id="doc008"
Uvicorn running on http://127.0.0.1:8000
```

---

# 8. API Access

## Main Endpoint

```text id="doc009"
http://127.0.0.1:8000
```

---

## Swagger Documentation

```text id="doc010"
http://127.0.0.1:8000/docs
```

---

# 9. Inventory API Development

## Temporary In-Memory Storage

```python id="doc011"
inventory = []
```

---

## Product Validation Model

```python id="doc012"
class Product(BaseModel):
    name: str
    quantity: int
    price: float
```

---

## GET Products Endpoint

```python id="doc013"
@app.get("/products")
```

Purpose:

* Retrieve all products

---

## POST Products Endpoint

```python id="doc014"
@app.post("/products")
```

Purpose:

* Add new products

---

# 10. Example Product JSON

```json id="doc015"
{
  "name": "Tomato",
  "quantity": 50,
  "price": 30
}
```

---

# 11. Understanding Duplicate Entries

## Observed Behavior

Products appeared multiple times.

Example:

```json id="doc016"
[
  {
    "name": "Tomato"
  },
  {
    "name": "Tomato"
  }
]
```

---

## Cause

POST endpoint executed multiple times.

Every POST request inserts new data:

```python id="doc017"
inventory.append(product.dict())
```

---

## Engineering Lesson

APIs execute exactly once per request.

Duplicate clicks create duplicate records.

---

# 12. PostgreSQL Installation

Installed:

* PostgreSQL 16
* pgAdmin 4

Configured:

* Port: `5433`

---

# 13. PostgreSQL Database Creation

Created database:

```text id="doc018"
cloudmart
```

Owner:

* postgres

---

# 14. Database Libraries Installation

## Install SQLAlchemy + PostgreSQL Driver

```bash id="doc019"
pip install sqlalchemy psycopg2-binary
```

---

# 15. Database Connection Configuration

## File

```text id="doc020"
database/connection.py
```

---

## Database Connection Code

```python id="doc021"
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:cloudmart123@localhost:5433/cloudmart"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

---

# 16. Database Connection Testing

## File

```text id="doc022"
test_connection.py
```

---

## Connection Test Code

```python id="doc023"
from database.connection import engine

try:
    connection = engine.connect()
    print("Database connected successfully!")
    connection.close()

except Exception as e:
    print("Connection failed!")
    print(e)
```

---

## Run Test

```bash id="doc024"
python test_connection.py
```

---

## Expected Output

```text id="doc025"
Database connected successfully!
```

---

# 17. SQLAlchemy ORM Model

## File

```text id="doc026"
database/models.py
```

---

## Product Table Model

```python id="doc027"
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
```

---

# 18. Table Creation Script

## File

```text id="doc028"
create_tables.py
```

---

## Table Creation Code

```python id="doc029"
from database.connection import engine
from database.models import Base

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
```

---

## Run Command

```bash id="doc030"
python create_tables.py
```

---

## Expected Output

```text id="doc031"
Creating database tables...
Tables created successfully!
```

---

# 19. pgAdmin Verification

Navigate:

```text id="doc032"
Servers
  ↓
PostgreSQL 16
  ↓
Databases
  ↓
cloudmart
  ↓
Schemas
  ↓
public
  ↓
Tables
```

Expected table:

```text id="doc033"
products
```

---

# 20. Core Concepts Learned

## FastAPI

Modern Python framework for APIs.

---

## API Endpoint

Example:

```python id="doc034"
@app.get("/")
```

Defines URL route handling.

---

## GET Request

Used to retrieve data.

---

## POST Request

Used to create/send data.

---

## JSON

Data format used between frontend and backend.

---

## PostgreSQL

Enterprise relational database system.

---

## SQLAlchemy

ORM that converts Python classes into SQL tables.

---

## ORM (Object Relational Mapper)

Converts:

```text id="doc035"
Python Objects
↕
SQL Tables
```

---

## Persistent Storage

Database retains data after restart unlike RAM lists.

---

# 21. Troubleshooting Guide

# Issue 1 — Virtual Environment Not Activating

## Symptoms

```text id="doc036"
venv not recognized
```

---

## Fix

Create environment:

```bash id="doc037"
python -m venv venv
```

Activate:

```bash id="doc038"
venv\Scripts\activate
```

---

# Issue 2 — FastAPI Server Not Running

## Symptoms

```text id="doc039"
uvicorn not recognized
```

OR

```text id="doc040"
No module named fastapi
```

---

## Cause

Packages not installed in virtual environment.

---

## Fix

Activate venv first:

```bash id="doc041"
venv\Scripts\activate
```

Install packages:

```bash id="doc042"
pip install fastapi uvicorn
```

---

# Issue 3 — Swagger Docs Not Opening

## Symptoms

Cannot access:

```text id="doc043"
http://127.0.0.1:8000/docs
```

---

## Cause

Backend server not running.

---

## Fix

Run:

```bash id="doc044"
uvicorn main:app --reload
```

---

# Issue 4 — Duplicate Product Entries

## Symptoms

Same products repeated.

---

## Cause

POST request executed multiple times.

---

## Understanding

Every POST request creates new record.

---

# Issue 5 — PostgreSQL Installed on Port 5433

## Situation

Database configured on:

```text id="doc045"
5433
```

instead of default:

```text id="doc046"
5432
```

---

## Fix

Update connection string accordingly:

```python id="doc047"
DATABASE_URL = "postgresql://postgres:password@localhost:5433/cloudmart"
```

---

# Issue 6 — Python Import Error

## Error

```text id="doc048"
ModuleNotFoundError: No module named 'database'
```

---

## Causes

* Wrong execution folder
* Missing package initialization
* Incorrect project structure

---

## Fixes Applied

Created:

```text id="doc049"
database/__init__.py
```

Correct structure:

```text id="doc050"
backend/
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── models.py
│
├── test_connection.py
├── main.py
└── venv/
```

Correct execution location:

```text id="doc051"
D:\cloudmart-project\backend
```

Correct command:

```bash id="doc052"
python test_connection.py
```

---

# Issue 7 — PostgreSQL Password Special Character

## Error

```text id="doc053"
could not translate host name "123@localhost"
```

---

## Cause

Password contained special character:

```text id="doc054"
@
```

Example problematic URL:

```text id="doc055"
postgresql://postgres:test@123@localhost:5433/cloudmart
```

---

## Fix

Changed password to:

```text id="doc056"
test123
```

Updated DATABASE_URL:

```python id="doc057"
DATABASE_URL = "postgresql://postgres:test123@localhost:5433/cloudmart"
```

---

# 22. Final Operational Status

## Successfully Completed

✅ FastAPI backend operational
✅ Swagger API docs operational
✅ Inventory API created
✅ PostgreSQL installed
✅ pgAdmin configured
✅ Database created
✅ SQLAlchemy configured
✅ Database connection successful
✅ ORM model created
✅ Product table created

---

# 23. Current Architecture

```text id="doc058"
Frontend/User
      ↓
FastAPI Backend
      ↓
SQLAlchemy ORM
      ↓
PostgreSQL Database
```

---

# 24. Next Session Roadmap

## Backend

* Save products permanently into PostgreSQL
* CRUD operations
* Product IDs
* Update/Delete APIs

---

## Frontend

* React setup
* API integration
* Dashboard UI

---

## DevOps

* Docker introduction
* GitHub workflow

---

## AWS

* EC2 deployment
* RDS integration
* IAM
* Security Groups

---

# 25. Engineering Lessons Learned

1. Backend systems are modular.
2. APIs and databases are separate layers.
3. ORM simplifies database operations.
4. Debugging is normal engineering work.
5. Folder structure matters in Python.
6. Connection strings are sensitive to formatting.
7. Incremental building creates strong foundations.

---

# CloudMart Status Report

## Backend Layer

ONLINE ✅

## Database Layer

ONLINE ✅

## ORM Layer

ONLINE ✅

## ERP Foundation

INITIALIZED ✅

