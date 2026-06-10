# CloudMart – Docker & Docker Compose Deployment Documentation

## Objective

The objective of this phase was to containerize the CloudMart backend application using Docker and orchestrate multiple services using Docker Compose.

This phase introduced:

* Docker fundamentals
* Docker images and containers
* Docker networking
* Persistent PostgreSQL storage using Docker volumes
* Multi-container orchestration using Docker Compose

---

# Architecture Overview

Current CloudMart architecture:

```text
Docker Compose Stack
 ├── backend-container
 └── postgres-container
```

The backend communicates with PostgreSQL through Docker’s internal network using automatic service discovery.

---

# Technologies Used

* Docker
* Docker Compose
* FastAPI
* PostgreSQL
* Python 3.11
* SQLAlchemy
* Uvicorn

---

# Phase 1 – Docker Installation

## Update Packages

```bash
sudo apt update
```

## Install Docker

```bash
sudo apt install docker.io -y
```

## Start Docker Service

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

## Verify Docker Installation

```bash
docker --version
```

---

# Phase 2 – Understanding Docker Concepts

## Important Concepts Learned

| Concept          | Description                            |
| ---------------- | -------------------------------------- |
| Docker Image     | Immutable blueprint/template           |
| Docker Container | Running instance of an image           |
| Dockerfile       | Instructions used to build images      |
| Volume           | Persistent storage for containers      |
| Docker Network   | Communication layer between containers |

---

# Phase 3 – Creating Backend Dockerfile

## Backend Directory

```bash
cd ~/cloudmart-project/backend
```

## Create Dockerfile

```bash
nano Dockerfile
```

## Dockerfile Content

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# Phase 4 – Creating .dockerignore

## Create File

```bash
nano .dockerignore
```

## Content

```text
venv
__pycache__
.git
```

## Purpose

Prevents unnecessary files from being copied into Docker images.

Benefits:

* Smaller image size
* Faster builds
* Cleaner runtime environment

---

# Phase 5 – Building Backend Docker Image

## Build Image

```bash
docker build -t cloudmart-backend .
```

## Verify Image

```bash
docker images
```

---

# Phase 6 – Docker Networking Concepts

## Important Discovery

Inside containers:

```text
localhost != EC2 localhost
```

Each container has:

* isolated networking
* isolated filesystem
* isolated runtime

This led to the need for Docker Compose and internal service discovery.

---

# Phase 7 – Docker Compose Introduction

Docker Compose was introduced to:

* orchestrate multiple containers
* create automatic networking
* simplify infrastructure management
* manage persistent storage

---

# Phase 8 – Creating docker-compose.yml

## Go to Project Root

```bash
cd ~/cloudmart-project
```

## Create Compose File

```bash
nano docker-compose.yml
```

## Compose File Content

```yaml
version: '3.9'

services:

  postgres:
    image: postgres:16
    container_name: postgres-container

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: cloudmart

    ports:
      - "5433:5432"

    volumes:
      - postgres-data:/var/lib/postgresql/data

  backend:
    build: ./backend
    container_name: backend-container

    ports:
      - "8000:8000"

    depends_on:
      - postgres

volumes:
  postgres-data:
```

---

# Phase 9 – Database Connection Configuration

## Update connection.py

File:

```text
backend/database/connection.py
```

## Database URL

```python
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/cloudmart"
```

---

# Important Networking Concept

## Internal Docker Communication

Containers communicate using:

* service names
* internal container ports

Example:

```text
postgres:5432
```

NOT:

```text
localhost
```

or:

```text
5433
```

---

# Phase 10 – Running Docker Compose

## Start Infrastructure

```bash
docker-compose up --build
```

## Verify Running Containers

```bash
docker ps
```

---

# Phase 11 – Common Issues Faced

## 1. localhost Connection Failure

### Problem

Backend container could not connect to PostgreSQL using localhost.

### Root Cause

Each container has isolated networking.

### Solution

Use Docker service name:

```text
postgres
```

instead of:

```text
localhost
```

---

## 2. PostgreSQL Volume Compatibility Error

### Problem

Old PostgreSQL data volume conflicted with newer PostgreSQL image version.

### Solution

Removed old volume and recreated it.

Commands:

```bash
docker-compose down

docker volume rm cloudmart-project_postgres-data
```

---

## 3. Port Mapping Confusion

### Important Difference

| External Host Port | Internal Container Port |
| ------------------ | ----------------------- |
| 5433               | 5432                    |

Containers communicate internally using:

```text
5432
```

---

## 4. Authentication Failure

### Problem

Incorrect password inside DATABASE_URL.

### Solution

Updated DATABASE_URL to:

```python
postgresql://postgres:postgres@postgres:5432/cloudmart
```

---

## 5. ContainerConfig Error

### Problem

Older docker-compose version caused:

```text
KeyError: 'ContainerConfig'
```

### Solution

Manually removed old containers:

```bash
docker rm -f backend-container postgres-container
```

Then restarted:

```bash
docker-compose up --build
```

---

# Final Outcome

Successfully deployed:

* PostgreSQL container
* FastAPI backend container
* Docker networking
* Persistent database storage
* Multi-container orchestration

---

# Major Concepts Learned

## Infrastructure as Code

Infrastructure configuration stored inside:

* Dockerfiles
* docker-compose.yml

---

## Service Discovery

Docker Compose automatically creates internal DNS.

Containers communicate using:

* service names
* internal ports

---

## Persistent Storage

Docker volumes allow PostgreSQL data persistence even after container removal.

---

# Future Enhancements

Planned next phases:

* Dockerized React frontend
* Nginx container
* HTTPS inside containers
* CI/CD pipeline
* Kubernetes deployment

---

# Conclusion

This phase transformed CloudMart from a manually deployed application into a containerized multi-service infrastructure.

Key areas learned:

* Docker fundamentals
* Container orchestration
* Networking
* Persistent storage
* Service discovery
* Infrastructure management

This phase forms the foundation for future Kubernetes and cloud-native deployments.
