# Day 37 – Docker Revision

## Self-Assessment Checklist

| Topic | Status |
|---|---|
| Run a container from Docker Hub (interactive + detached) | ✅ can do |
| List, stop, remove containers and images | ✅ can do |
| Explain image layers and how caching works | ✅ can do |
| Write a Dockerfile from scratch (FROM, RUN, COPY, WORKDIR, CMD) | ✅ can do |
| Explain CMD vs ENTRYPOINT | ✅ can do |
| Build and tag a custom image | ✅ can do |
| Create and use named volumes | ✅ can do |
| Use bind mounts | ✅ can do |
| Create custom networks and connect containers | ✅ can do |
| Write a docker-compose.yml for a multi-container app | ✅ can do |
| Use environment variables and .env files in Compose | ✅ can do |
| Write a multi-stage Dockerfile | ✅ can do |
| Push an image to Docker Hub | ✅ can do |
| Use healthchecks and depends_on | ✅ can do |

---

## Quick-Fire Questions — Answers

**1. What is the difference between an image and a container?**

An image is a read-only, layered blueprint — it defines the filesystem, dependencies, and default runtime config. A container is a live, running instance of that image with its own writable layer on top. You can run multiple containers from the same image; they don't affect each other or the image itself.

**2. What happens to data inside a container when you remove it?**

It's gone. A container's writable layer is ephemeral — it only exists while the container exists. Once you `docker rm` a container, anything written inside it (that wasn't in a volume or bind mount) is permanently deleted. This is why volumes exist.

**3. How do two containers on the same custom network communicate?**

By container name. Docker's built-in DNS resolves container names to their internal IP addresses automatically — but only on user-defined networks (not the default `bridge`). So if a Flask container needs to reach a MySQL container named `db`, it connects to `mysql://db:3306`. No manual IP management needed.

**4. What does `docker compose down -v` do differently from `docker compose down`?**

`docker compose down` stops and removes containers and the networks Compose created. `docker compose down -v` does all of that and also deletes the named volumes defined in the Compose file. This means database data, uploaded files, anything stored in those volumes — permanently wiped. Use it carefully.

**5. Why are multi-stage builds useful?**

They let you separate the build environment from the runtime environment. In a typical build, you need compilers, build tools, and dev dependencies that have no place in production. With multi-stage builds, Stage 1 does all the heavy lifting (compiling, installing), and Stage 2 copies only the final artifact into a minimal base image. The result is a smaller, leaner, more secure production image.

**6. What is the difference between `COPY` and `ADD`?**

Both copy files into the image. `COPY` is straightforward — it copies local files and directories only. `ADD` does the same but also supports fetching remote URLs and auto-extracting `.tar` archives. In practice, always prefer `COPY` for clarity and predictability. Use `ADD` only when you specifically need its extra capabilities.

**7. What does `-p 8080:80` mean?**

It maps port 8080 on the host to port 80 inside the container. Traffic hitting `localhost:8080` on your machine is forwarded to whatever is listening on port 80 inside the container. Format is always `host_port:container_port`.

**8. How do you check how much disk space Docker is using?**

```bash
docker system df
```

This shows a breakdown of disk usage by images, containers, volumes, and build cache — including what's "reclaimable" (safe to prune). For a more detailed view per object, add the `-v` flag: `docker system df -v`.

---

## Revisit Weak Spots

*(Pick 2 topics you marked as shaky and redo the hands-on tasks.)*

### Topic 1 — Healthchecks and depends_on

The key thing to internalize: `depends_on: condition: service_healthy` waits for the healthcheck to pass before starting the dependent service — but it does NOT guarantee the application inside is ready. A MySQL container can pass a `mysqladmin ping` healthcheck before it's accepting connections on port 3306 for your schema.

**Hands-on task:**

```yaml
# docker-compose.yml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: testdb
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "5000:5000"
```

Pair this with retry logic in the app itself — healthchecks and retry logic solve different problems and both are needed.

---

### Topic 2 — Multi-Stage Builds with Distroless

The part that trips people up: installing dependencies with `--target` and setting `PYTHONPATH` correctly so the distroless stage can find them.

**Hands-on task:**

```dockerfile
# Stage 1 — Builder
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/python-deps -r requirements.txt
COPY app.py .

# Stage 2 — Production
FROM gcr.io/distroless/python3-debian12

WORKDIR /app
COPY --from=builder /python-deps /python-deps
COPY --from=builder /app/app.py .

ENV PYTHONPATH=/python-deps

EXPOSE 5000
CMD ["app.py"]
```

Verify: `docker images` — compare the size of this image against a plain `python:3.11-slim` build of the same app. The difference should be ~90MB+.

---

## What Days 29–36 Actually Covered

| Day | Topic |
|---|---|
| 29 | Docker fundamentals — images, containers, basic commands |
| 30 | Dockerfile — writing from scratch, layers, caching |
| 31 | Volumes and bind mounts — data persistence |
| 32 | Networking — bridge, host, custom networks, container DNS |
| 33 | Docker Compose — multi-container apps, services, networks |
| 34 | Docker Compose — env vars, .env files, overrides |
| 35 | Multistage builds, distroless, non-root user |
| 36 | End-to-end Flask + MySQL app — healthchecks, retry logic, Docker Hub |