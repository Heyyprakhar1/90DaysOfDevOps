# Day 33 – Docker Compose: Multi-Container Applications

### Task 1: Install & Verify

1. Check if Docker Compose is available on your machine
2. Verify the version

```bash
docker compose version
# Expected output: Docker Compose version v2.x.x
```

---

### Task 2: My  First Compose File

1. Create a folder `compose-basics`
2. Write a `docker-compose.yml` that runs a single **Nginx** container with port mapping

```bash
mkdir compose-basics && cd compose-basics
```

**`docker-compose.yml`:**
```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
```

3. Start it:
```bash
docker compose up
```

4. Open your browser → `http://localhost:8080`
5. Stop it:
```bash
docker compose down
```

---

### Task 3: Two-Container Setup

Write a `docker-compose.yml` that runs:
- A **WordPress** container
- A **MySQL** container

volumes:
  mysql-data:
```

**Key points:**
- Compose creates a default network automatically — both services are on it
- `db` in `WORDPRESS_DB_HOST` is the **service name**, which acts as the DNS hostname
- The named volume `db_data` persists MySQL data across restarts

**Start and set up WordPress:**
```bash
docker compose up -d
# Open http://localhost:8080 and complete the WordPress setup wizard
```

**Verify data persistence:**
```bash
docker compose down
docker compose up -d
# Open http://localhost:8080 — your WordPress data should still be there ✅
```

---

### Task 4: Compose Commands

| Goal | Command |
|------|---------|
| Start in detached mode | `docker compose up -d` |
| View running services | `docker compose ps` |
| View logs of all services | `docker compose logs -f` |
| View logs of a specific service | `docker compose logs -f wordpress` |
| Stop services (keep containers) | `docker compose stop` |
| Remove containers & networks | `docker compose down` |
| Remove containers, networks & volumes | `docker compose down -v` |
| Rebuild images after a change | `docker compose up -d --build` |

---

### Task 5: Environment Variables

**Option A – Inline in `docker-compose.yml`:**
```yaml
services:
  wordpress:
    image: wordpress:latest
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wpuser
      WORDPRESS_DB_PASSWORD: wppassword
```

**Option B – Using a `.env` file:**

Create `.env` in the same directory as your `docker-compose.yml`:
```dotenv
DB_NAME=wordpress
DB_USER=wpuser
DB_PASSWORD=wppassword
DB_ROOT_PASSWORD=rootpassword
```

Reference variables in `docker-compose.yml`:
```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}

  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_NAME: ${DB_NAME}
      WORDPRESS_DB_USER: ${DB_USER}
      WORDPRESS_DB_PASSWORD: ${DB_PASSWORD}
    depends_on:
      - db
```

**Verify variables are picked up:**
```bash
docker compose config
# Prints the resolved compose file with all variables substituted
```

---

## Quick Reference

```bash
docker compose up -d          # Start detached
docker compose down           # Stop & remove containers/networks
docker compose logs -f        # Follow all logs
docker compose ps             # List running services
docker compose exec <svc> sh  # Shell into a running container
```

**Key concepts:**
- Compose creates a **default network** for all services automatically
- **Service names** are the DNS hostnames containers use to talk to each other
- Named **volumes** persist data across `docker compose down` (removed only with `-v`)
- `.env` files are automatically loaded — no extra configuration needed
