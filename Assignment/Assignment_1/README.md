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

Run this **once** on the host before `docker compose up`.

> Replace `eth0` with your actual host network interface (check with `ip link`).
> Replace `192.168.1.0/24` and `192.168.1.1` with your LAN subnet and gateway.
> The `--aux-address` reserves the host IP so Docker won't assign it to a container.

```bash
docker network create \
  --driver macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  --aux-address="host=192.168.1.1" \
  -o parent=eth0 \
  macvlan_net
```

Verify the network was created:

```bash
docker network inspect macvlan_net
```

---

## Step 2 — Configure Environment Variables

Copy `.env` and update the password:

```bash
cp .env .env.local   # optional local override
```

The `.env` file already contains sensible defaults. **Change `POSTGRES_PASSWORD`** before deploying.

---

## Step 3 — Build and Start

```bash
docker compose up --build -d
```

Check that both containers are running and healthy:

```bash
docker compose ps
```

---

## Step 4 — Test the API

Both containers get static LAN IPs so they are reachable directly from any device on the LAN.

| Container | Static IP      | Port |
|-----------|----------------|------|
| backend   | 192.168.1.100  | 8000 |
| db        | 192.168.1.101  | 5432 |

### Healthcheck
```bash
curl http://192.168.1.100:8000/health
# → {"status":"ok","database":"connected"}
```

### Insert a record (POST)
```bash
curl -X POST http://192.168.1.100:8000/records \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "value": "Hello from LAN!"}'
```

### Fetch all records (GET)
```bash
curl http://192.168.1.100:8000/records
```

### Interactive API docs
Open in browser: **http://192.168.1.100:8000/docs**

---

## Volume Persistence Test

```bash
# 1. Insert a record
curl -X POST http://192.168.1.100:8000/records \
  -H "Content-Type: application/json" \
  -d '{"name": "PersistTest", "value": "still here after restart"}'

# 2. Stop and remove containers (NOT the volume)
docker compose down

# 3. Restart
docker compose up -d

# 4. Fetch records — PersistTest should still be there
curl http://192.168.1.100:8000/records
```

To also remove the volume (wipes data):

```bash
docker compose down -v
```

---

## Macvlan Host Isolation Workaround

With macvlan, **the host machine cannot reach the containers** by default (kernel restriction).  
To fix this, create a macvlan sub-interface on the host:

```bash
# Create a macvlan interface on the host side
sudo ip link add macvlan_host link eth0 type macvlan mode bridge
sudo ip addr add 192.168.1.200/32 dev macvlan_host
sudo ip link set macvlan_host up

# Add a route so the host can reach the container subnet
sudo ip route add 192.168.1.0/24 dev macvlan_host
```

After this, `curl http://192.168.1.100:8000/health` works from the host too.  
**This workaround is not persistent across reboots** — add it to `/etc/rc.local` or a systemd unit if needed.

---

## Useful Commands

```bash
# View logs
docker compose logs -f backend
docker compose logs -f db

# Inspect container IPs
docker inspect project_backend | grep IPAddress
docker inspect project_db | grep IPAddress

# Check network
docker network inspect macvlan_net

# Stop everything (keep volume)
docker compose down

# Stop and delete volume (data lost!)
docker compose down -v
```

---

## Image Size Comparison

After building, compare image sizes:

```bash
docker images | grep project
```

Expected approximate sizes (multi-stage build benefit):

| Image             | Approx Size | Notes                          |
|-------------------|-------------|--------------------------------|
| backend (runtime) | ~80 MB      | Only venv + libpq, no compiler |
| db (runtime)      | ~90 MB      | postgres:16-alpine             |

Without multi-stage (single-stage with build tools): ~300+ MB for the backend.
