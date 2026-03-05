# Day 34 – Docker Compose: Real-World Multi-Container Apps

## Project Overview

Built a production-style 3-service application stack using Docker Compose:

- Flask Web Application
- MySQL Database
- Redis Cache

The application verifies connectivity with MySQL and Redis and displays a success message in the browser.

---

## Project Structure

2026/day-34/
│
├── docker-compose.yml
├── day-34-compose-advanced.md
└── app/
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py
    └── templates/
        └── index.html

---

# Task 1: Build Your Own App Stack

Created a 3-service Docker Compose setup:

### Services:
- **web** → Flask app built from custom Dockerfile
- **db** → MySQL 8
- **redis** → Redis 7

The Flask app:
- Connects to MySQL
- Pings Redis
- Displays connectivity status on webpage

---

# Task 2: depends_on & Healthchecks

### 1️⃣ depends_on with condition

Used:

depends_on:
  db:
    condition: service_healthy

This ensures:
- Flask waits until MySQL is fully ready
- Not just container started

---

### 2️⃣ MySQL Healthcheck

healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 5s
  timeout: 3s
  retries: 5

---

### 3️⃣ Test Result

After:

docker compose down
docker compose up --build

✔ Flask waited for DB to become healthy  
✔ No connection errors on startup  

---

# Task 3: Restart Policies

### restart: always
- Database restarts automatically
- Even after manual kill
- Recommended for stateful production services

### restart: on-failure
- Restarts only if container exits with non-zero status
- Does NOT restart if manually stopped
- Useful for batch jobs or retry-based apps

### Testing

docker kill mysql-db  
→ Container restarted automatically (restart: always)

docker stop mysql-db  
→ Did not restart when using on-failure

---

# Task 4: Custom Dockerfiles in Compose

Used:

build: ./app

Instead of prebuilt image.

Rebuilt with:

docker compose up --build -d

 Code changes reflected immediately  
 Single command rebuild + restart  

---

# Task 5: Named Networks & Volumes

### Custom Network

networks:
  app-network:
    driver: bridge

All services attached explicitly.

---

### Named Volume (Data Persistence)

volumes:
  mysql-data:

Mapped to:

/var/lib/mysql

Database data persists across container restarts  

---

### Labels Added

labels:
  project: "day-34"
  tier: "database"

Improves service organization and metadata visibility.

---

# Task 6: Scaling (Bonus)

Tried:

docker compose up --scale web=3

### Result:

 Port binding error

Reason:
- Port 5000 mapped to host
- Only one container can bind a host port
- Multiple replicas cannot map same host port

---

### Why Simple Scaling Fails

Docker Compose (non-swarm mode):
- Does not include built-in load balancing
- Host ports cannot be duplicated

### Production Solution

- Use reverse proxy (Nginx / Traefik)
- Remove host port binding and expose internally
- Use Docker Swarm or Kubernetes

---

# Key Learnings

- Multi-container orchestration
- Service dependency management
- Health-based startup sequencing
- Restart behavior understanding
- Persistent storage with named volumes
- Custom Docker builds
- Horizontal scaling limitations
- Real-world 3-tier architecture

---

# Final Output

Browser Output:

🚀 Welcome to Day-34 Assignment

MySQL Connection Successful ✅  
Redis Connection Successful ✅  

---
