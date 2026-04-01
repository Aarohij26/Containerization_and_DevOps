# Project Assignment 1

## Containerized FastAPI + PostgreSQL with Docker Compose & Macvlan

---

## Project Structure

```
project/
├── backend/
│   ├── Dockerfile          # Multi-stage: builder → runtime (python:3.12-alpine)
│   ├── main.py             # FastAPI app (POST /records, GET /records, GET /health)
│   ├── requirements.txt
│   └── .dockerignore
├── database/
│   ├── Dockerfile          # Multi-stage: config-builder → postgres:16-alpine
│   ├── init.sql            # Auto-runs on first container startup
│   └── .dockerignore
├── docker-compose.yml
├── .env                    # Secrets — DO NOT commit to Git
└── README.md
```

---

## Step 1 — Create the Macvlan Network

```bash
docker network create \
  --driver macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  --aux-address="host=192.168.1.1" \
  -o parent=eth0 \
  macvlan_net
```

[Network](./Images/image1.png)

---

## Verify Network

```bash
docker network inspect macvlan_net
```

[Inspect](./Images/image1.png)

---

## Step 2 — Configure Environment Variables

```bash
cp .env .env.local
```

[Environment](./Images/image3.png)

---

## Step 3 — Build and Start Containers

```bash
docker compose up --build -d
```

[Build](./Images/image4.png)

```bash
docker compose ps
```

[Compose](./Images/image5.png)

---

## Step 4 — Test the API

### Health Check

```bash
curl http://192.168.1.100:8000/health
```

[Health](./Images/image6.png)

### Insert Record

```bash
curl -X POST http://192.168.1.100:8000/records \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "value": "Hello"}'
```

[Record](./Images/image7.png)

### Fetch Records

```bash
curl http://192.168.1.100:8000/records
```

## Volume Persistence Test

```bash
docker compose down
docker compose up -d
```

[Persistence](./Images/image8.png)

---

## Macvlan Fix

```bash
sudo ip link add macvlan_host link eth0 type macvlan mode bridge
```

[fix](./Images/image9.png)

---

## Image Size

```bash
docker images
```

[Images](./Images/image11.png)

---
## Useful Commands

```bash
# View logs
docker compose logs -f backend
docker compose logs -f db
```
[Logs](./Images/image10.png)

---
# Inspect container IPs
docker inspect project_backend | grep IPAddress
docker inspect project_db | grep IPAddress

[IPs](./Images/image12.png)
```
---

## Image Size Comparison

After building, compare image sizes:

```bash
docker images | grep project
```
[Images](./Images/image13.png)

Expected approximate sizes (multi-stage build benefit):

| Image             | Approx Size | Notes                          |
|-------------------|-------------|--------------------------------|
| backend (runtime) | ~80 MB      | Only venv + libpq, no compiler |
| db (runtime)      | ~90 MB      | postgres:16-alpine             |

Without multi-stage (single-stage with build tools): ~300+ MB for the backend.
