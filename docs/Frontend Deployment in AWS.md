# CloudMart React Frontend Deployment on AWS EC2

## Project

CloudMart ERP System

## Objective

Deploy the React frontend application to AWS EC2 and integrate it with:

* Nginx
* FastAPI backend
* PostgreSQL database
* HTTPS infrastructure

---

# 1. Frontend Deployment Architecture

## Final Production Architecture

```text id="hwb9qf"
Browser
    ↓ HTTPS
Nginx
    ├── React Frontend
    └── FastAPI Backend API
            ↓
        PostgreSQL
```

---

# 2. Existing Infrastructure Prerequisites

Before frontend deployment, the following components were already operational:

| Component               | Status     |
| ----------------------- | ---------- |
| AWS EC2 Ubuntu Server   | Configured |
| FastAPI Backend         | Running    |
| PostgreSQL Database     | Running    |
| Nginx Reverse Proxy     | Configured |
| HTTPS Self-Signed SSL   | Configured |
| systemd Backend Service | Active     |

---

# 3. Install Node.js on EC2

## Initial Problem

Ubuntu default repositories installed:

```text id="dhlfkk"
Node.js v18.19.1
```

Modern Vite versions required:

```text id="xzt9p6"
Node.js 20+
```

Resulting error:

```text id="fq6jsr"
Vite requires Node.js version 20.19+ or 22.12+
```

---

# 4. Remove Old Node.js Installation

## Remove Existing Packages

```bash id="wclb75"
sudo apt remove nodejs npm -y
```

---

## Remove Unused Dependencies

```bash id="bc6ex7"
sudo apt autoremove -y
```

---

# 5. Install Modern Node.js

## Install curl

```bash id="t2c9db"
sudo apt install curl -y
```

---

## Add Official NodeSource Repository

```bash id="r1v0be"
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
```

---

## Install Node.js 22

```bash id="ayk1x4"
sudo apt install nodejs -y
```

---

## Verify Installation

```bash id="3quqko"
node -v
npm -v
```

Expected:

```text id="4v7v1h"
v22.x.x
```

---

# 6. Install Frontend Dependencies

## Navigate to Frontend Directory

```bash id="9r1w6u"
cd ~/cloudmart-project/frontend
```

---

## Remove Old Dependencies

```bash id="f8xkde"
rm -rf node_modules package-lock.json
```

---

## Install Packages

```bash id="prb95y"
npm install
```

---

# 7. Production Frontend Build

## Build React Application

```bash id="0g39n8"
npm run build
```

---

## Build Output

Successful build generated:

```text id="7v2g0v"
dist/
```

directory.

---

# 8. Frontend API Configuration

## Production API Change

### Local Development API

```javascript id="ij8d7y"
http://127.0.0.1:8000/products
```

---

### Production API

```javascript id="smpm2i"
/products
```

---

# Why Relative Path Was Required

In production:

* frontend and backend share same domain/IP
* Nginx routes requests internally
* avoids CORS issues
* creates cleaner architecture

---

# 9. Configure Nginx for Frontend + Backend

## Open Nginx Configuration

```bash id="ag8nkm"
sudo nano /etc/nginx/sites-available/default
```

---

# 10. Final Nginx Configuration

```nginx id="ycfx2x"
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

    root /home/ubuntu/cloudmart-project/frontend/dist;

    index index.html;

    location / {

        try_files $uri /index.html;
    }

    location /products {

        proxy_pass http://127.0.0.1:8000/products;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /docs {

        proxy_pass http://127.0.0.1:8000/docs;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /openapi.json {

        proxy_pass http://127.0.0.1:8000/openapi.json;

        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

# 11. Nginx Configuration Explanation

| Path            | Purpose                   |
| --------------- | ------------------------- |
| `/`             | Serve React frontend      |
| `/products`     | Proxy FastAPI product API |
| `/docs`         | Proxy Swagger UI          |
| `/openapi.json` | Proxy FastAPI schema      |

---

# 12. Test Nginx Configuration

## Validate Syntax

```bash id="t5nt2y"
sudo nginx -t
```

Expected:

```text id="2p5bkk"
syntax is ok
test is successful
```

---

## Restart Nginx

```bash id="r8sccf"
sudo systemctl restart nginx
```

---

# 13. Production Deployment Issue

## Error Encountered

Browser displayed:

```text id="b9kxsn"
500 Internal Server Error
```

---

# Root Cause Analysis

Nginx could not access frontend files due to Linux permission restrictions.

Frontend build location:

```text id="vw13k5"
/home/ubuntu/cloudmart-project/frontend/dist
```

Nginx runs under:

```text id="6mqw7z"
www-data
```

user.

---

# 14. Debugging Process

## Check Nginx Logs

```bash id="bxftiv"
sudo tail -f /var/log/nginx/error.log
```

---

## Verify dist Folder

```bash id="3o9uqj"
ls ~/cloudmart-project/frontend/dist
```

---

# 15. Fix Linux Permissions

## Grant Read Permissions

```bash id="e8lkr5"
sudo chmod -R 755 /home/ubuntu/cloudmart-project
```

---

## Allow Nginx Access to Home Directory

```bash id="mjlwm7"
sudo chmod -R 755 /home/ubuntu
```

---

# Why This Fixed the Problem

Linux permissions now allowed:

* Nginx (`www-data`)
* to read frontend build files
* and serve React application successfully

---

# 16. Final Production Verification

## Restart Nginx

```bash id="qu6w7s"
sudo systemctl restart nginx
```

---

## Access Application

```text id="vxlx7o"
https://YOUR_PUBLIC_IP
```

---

# 17. Final Successful Deployment

## CloudMart Production Stack

### Frontend

✅ React deployed successfully

### Backend

✅ FastAPI operational

### Database

✅ PostgreSQL operational

### Reverse Proxy

✅ Nginx configured

### HTTPS

✅ Self-signed SSL active

### Linux Services

✅ systemd backend service operational

---

# 18. Final Production Architecture

```text id="fg8q7x"
Browser
    ↓ HTTPS
Nginx
    ├── React Frontend
    └── FastAPI Backend
            ↓
        PostgreSQL
```

---

# 19. Key Concepts Learned

## React Production Build

```text id="t1lq6f"
npm run build
```

creates optimized static frontend files.

---

## Nginx Static File Hosting

Nginx serves React frontend directly from:

```text id="d7k4bx"
dist/
```

directory.

---

## Reverse Proxy Architecture

Nginx routes:

* frontend requests
* backend API requests
* Swagger requests

through single public endpoint.

---

## Relative API Paths

Using:

```javascript id="b0olbm"
/products
```

instead of localhost URLs enables production deployment.

---

## Linux File Permissions

Nginx required read access to:

* React build files
* parent directories

---

## Production Infrastructure Debugging

Key debugging tools:

* nginx logs
* permission checks
* path validation
* service status verification

---

# 20. Current CloudMart Infrastructure Status

| Component       | Status      |
| --------------- | ----------- |
| AWS EC2         | Running     |
| React Frontend  | Public      |
| FastAPI Backend | Public      |
| PostgreSQL      | Running     |
| HTTPS           | Enabled     |
| Nginx           | Operational |
| systemd         | Operational |

---

# 21. Next Planned Phase

## Docker & Containerization

Upcoming objectives:

* Dockerize backend
* Dockerize frontend
* docker-compose orchestration
* containerized deployment
* DevOps workflow foundation

---
