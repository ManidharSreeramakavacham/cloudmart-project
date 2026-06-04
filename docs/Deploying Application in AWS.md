# CloudMart AWS Deployment & Production Hardening Documentation

## Project

CloudMart ERP System

## Objective

Deploy the CloudMart backend application from local environment to AWS cloud infrastructure using:

* AWS EC2
* Ubuntu Linux
* FastAPI
* PostgreSQL
* Nginx Reverse Proxy
* systemd Service Management
* Self-Signed SSL Certificate

---

# 1. Architecture Overview

## Initial Cloud Architecture

```text
Internet
    ↓
AWS EC2 Ubuntu Server
    ↓
FastAPI Backend
    ↓
PostgreSQL Database
```

---

## Production Hardened Architecture

```text
HTTPS
    ↓
Nginx Reverse Proxy
    ↓
FastAPI Backend (systemd managed)
    ↓
PostgreSQL Database
```

---

# 2. AWS EC2 Instance Creation

## Step 1 — Open AWS EC2 Dashboard

Navigate to:

* AWS Console
* EC2 Service

---

## Step 2 — Launch Instance

### Instance Configuration

| Setting          | Value                    |
| ---------------- | ------------------------ |
| Name             | cloudmart-backend-server |
| Operating System | Ubuntu Server 24.04 LTS  |
| Instance Type    | t2.micro                 |

---

## Step 3 — Create Key Pair

### Key Pair Configuration

| Setting | Value         |
| ------- | ------------- |
| Name    | cloudmart-key |
| Type    | RSA           |
| Format  | .pem          |

Downloaded file:

```text
cloudmart-key.pem
```

Important:

* Never upload `.pem` file publicly
* Never commit `.pem` to GitHub

---

## Step 4 — Configure Security Group

### Initial Inbound Rules

| Type | Port |
| ---- | ---- |
| SSH  | 22   |
| HTTP | 80   |

---

## Step 5 — Launch Instance

After launch:

* Wait until instance state becomes `Running`
* Copy Public IPv4 address

Example:

```text
13.xx.xx.xx
```

---

# 3. SSH Into EC2 Server

## Step 1 — Move Key File

Recommended path:

```text
D:\aws-keys
```

---

## Step 2 — Connect Using SSH

```bash
ssh -i cloudmart-key.pem ubuntu@YOUR_PUBLIC_IP
```

Example:

```bash
ssh -i cloudmart-key.pem ubuntu@13.xx.xx.xx
```

---

## Step 3 — Accept First Connection

When prompted:

```text
Are you sure you want to continue connecting?
```

Type:

```text
yes
```

---

## Successful Login Output

```text
ubuntu@ip-xxx:~$
```

---

# 4. Linux Server Preparation

## Update Linux Packages

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Install Required Tools

```bash
sudo apt install python3-pip python3-venv git -y
```

---

## Verify Installation

```bash
python3 --version
git --version
```

---

# 5. Clone CloudMart Repository

## Clone GitHub Repository

```bash
git clone https://github.com/ManidharSreeramakavacham/cloudmart-project.git
```

---

## Enter Backend Directory

```bash
cd cloudmart-project/backend
```

---

# 6. Create Python Virtual Environment

## Create Virtual Environment

```bash
python3 -m venv venv
```

---

## Activate Virtual Environment

```bash
source venv/bin/activate
```

Expected:

```text
(venv)
```

---

# 7. Install Python Dependencies

## Install Requirements

```bash
pip install -r requirements.txt
```

Installed:

* FastAPI
* SQLAlchemy
* psycopg2-binary
* uvicorn

---

# 8. PostgreSQL Installation on EC2

## Install PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y
```

---

## Start PostgreSQL Service

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

---

# 9. PostgreSQL Database Setup

## Enter PostgreSQL Shell

```bash
sudo -u postgres psql
```

---

## Create CloudMart Database

```sql
CREATE DATABASE cloudmart;
```

---

## Set PostgreSQL Password

```sql
ALTER USER postgres PASSWORD 'cloudmart123';
```

---

## Exit PostgreSQL

```sql
\q
```

---

# 10. Configure Database Connection

## Open connection.py

```bash
nano database/connection.py
```

---

## DATABASE_URL Configuration

```python
DATABASE_URL = "postgresql://postgres:cloudmart123@localhost:5432/cloudmart"
```

Important:

* Linux PostgreSQL default port is `5432`
* Local Windows setup previously used `5433`

---

# 11. Create Database Tables

## Run Table Creation Script

```bash
python create_table.py
```

Expected:

```text
Database tables created successfully!
```

---

# 12. Run FastAPI Backend

## Start Uvicorn

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Important:

```text
0.0.0.0
```

allows external access.

---

# 13. Open FastAPI Port in Security Group

## Add Inbound Rule

| Type       | Port |
| ---------- | ---- |
| Custom TCP | 8000 |

Source:

```text
0.0.0.0/0
```

---

## Test Swagger UI

```text
http://YOUR_PUBLIC_IP:8000/docs
```

---

# 14. Install Nginx Reverse Proxy

## Install Nginx

```bash
sudo apt install nginx -y
```

---

## Start and Enable Nginx

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## Verify Nginx Status

```bash
sudo systemctl status nginx
```

Expected:

```text
active (running)
```

---

## Test Nginx

Open browser:

```text
http://YOUR_PUBLIC_IP
```

Expected:

```text
Welcome to nginx!
```

---

# 15. Configure Nginx Reverse Proxy

## Open Default Nginx Config

```bash
sudo nano /etc/nginx/sites-available/default
```

---

## Nginx Reverse Proxy Configuration

```nginx
server {

    listen 80;

    server_name _;

    location / {

        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Test Nginx Configuration

```bash
sudo nginx -t
```

Expected:

```text
syntax is ok
test is successful
```

---

## Restart Nginx

```bash
sudo systemctl restart nginx
```

---

## Test Reverse Proxy

```text
http://YOUR_PUBLIC_IP/docs
```

---

# 16. Configure systemd Service

## Create Service File

```bash
sudo nano /etc/systemd/system/cloudmart.service
```

---

## Service Configuration

```ini
[Unit]
Description=CloudMart FastAPI Backend
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/cloudmart-project/backend

ExecStart=/home/ubuntu/cloudmart-project/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Reload systemd

```bash
sudo systemctl daemon-reload
```

---

## Start Service

```bash
sudo systemctl start cloudmart
```

---

## Enable Auto-Start

```bash
sudo systemctl enable cloudmart
```

---

## Verify Service Status

```bash
sudo systemctl status cloudmart
```

Expected:

```text
active (running)
```

---

# 17. Self-Signed SSL Certificate Setup

## Create SSL Directory

```bash
sudo mkdir -p /etc/nginx/ssl
```

---

## Generate Self-Signed Certificate

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout /etc/nginx/ssl/cloudmart.key \
-out /etc/nginx/ssl/cloudmart.crt
```

---

## Certificate Information

Use:

* Organization: CloudMart
* Common Name: EC2 Public IP

Example:

```text
13.xx.xx.xx
```

---

# 18. Configure HTTPS in Nginx

## Open Nginx Config

```bash
sudo nano /etc/nginx/sites-available/default
```

---

## HTTPS Nginx Configuration

```nginx
server {

    listen 80;

    server_name _;

    return 301 https://$host$request_uri;
}

server {

    listen 443 ssl;

    server_name _;

    ssl_certificate /etc/nginx/ssl/cloudmart.crt;

    ssl_certificate_key /etc/nginx/ssl/cloudmart.key;

    location / {

        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

# 19. Open HTTPS Port

## Add Security Group Rule

| Type  | Port |
| ----- | ---- |
| HTTPS | 443  |

Source:

```text
0.0.0.0/0
```

---

# 20. Verify HTTPS Configuration

## Test Nginx

```bash
sudo nginx -t
```

---

## Restart Nginx

```bash
sudo systemctl restart nginx
```

---

## Test HTTPS

```text
https://YOUR_PUBLIC_IP/docs
```

Browser warning expected:

```text
Connection is not private
```

This is normal for self-signed certificates.

Proceed manually through browser warning.

---

# 21. Final Production Architecture

```text
HTTPS
    ↓
Nginx SSL Termination
    ↓
FastAPI Backend (systemd managed)
    ↓
PostgreSQL Database
```

---

# 22. Key Concepts Learned

## EC2

Virtual Linux server in AWS cloud.

---

## SSH

Remote server administration protocol.

---

## Security Groups

AWS cloud firewall configuration.

---

## Reverse Proxy

Nginx forwarding traffic to FastAPI.

---

## systemd

Linux service manager for production processes.

---

## SSL/TLS

Encrypted HTTPS communication.

---

## Self-Signed Certificates

Locally trusted encryption certificates.

---

## Production Hardening

Improving deployment reliability and security.

---

# 23. Current CloudMart Status

## Backend

✅ Publicly deployed

## Database

✅ Persistent PostgreSQL operational

## Nginx

✅ Reverse proxy active

## systemd

✅ Auto-restart enabled

## HTTPS

✅ Self-signed SSL configured

## AWS Infrastructure

✅ Production-style architecture operational

---

# 24. Next Planned Phase

## React Frontend Deployment

Upcoming goals:

* Deploy React frontend
* Serve frontend through Nginx
* Connect public frontend ↔ backend
* Full cloud-hosted ERP application

---
