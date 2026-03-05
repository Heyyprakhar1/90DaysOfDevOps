# Day 36 – End-to-End Dockerized Flask + MySQL Application

## Application Overview

For this project, I chose a **Flask + MySQL feedback application**. It builds naturally on my earlier 2-tier To-Do app and provided the right scope to demonstrate a full containerization workflow without the business logic getting in the way.

The app lets users submit feedback (name, message, rating), stores it in MySQL, displays all entries, and calculates an average rating. It automatically creates the required table on startup and includes retry logic to handle database readiness timing — making it resilient to the natural startup race condition between containers.

---

## Dockerfile Strategy

I implemented two approaches to cover both production optimization and secure container design.

### Approach 1 — Multi-Stage Build with Distroless Image

**Stage 1 (Builder):** `python:3.11-slim`
- Installed dependencies into `/python-deps` using `--target`
- Copied application code

**Stage 2 (Production):** `gcr.io/distroless/python3-debian12`
- Copied only the installed dependencies and app file
- Set `PYTHONPATH` explicitly
- No shell, no package manager, no unnecessary OS components

Distroless was chosen for its reduced attack surface and significantly smaller footprint — the final image came in at **~74.8 MB vs ~167 MB** for the slim-based build.

### Approach 2 — Slim Image with Non-Root User

Using `python:3.11-slim` as the base, this approach focused on secure container design:

- Created a custom group and user
- Changed ownership of `/app` before switching context
- Applied `USER` directive after file copy
- Exposed only the required port

---

## Multi-Stage Build Challenges

This was the most demanding part of the project. Three distinct problems surfaced:

**Problem 1 — Dependency copying between stages**
Installing packages with `--target` and carrying them across stages required precise folder structure and an explicit `PYTHONPATH`. Initially, Python couldn't locate the installed packages at runtime.

> **Fix:** Installed into `/python-deps`, copied that folder explicitly into Stage 2, and set `ENV PYTHONPATH=/python-deps`.

**Problem 2 — Debugging a distroless runtime**
Distroless images have no shell — you cannot `exec` into them or run `sh` for inspection. This caused significant friction when something wasn't working post-build.

> **Fix:** Verified all dependencies locally in the slim image first, confirmed correct `CMD` format, then switched to distroless only after the build was stable.

**Problem 3 — Non-root permission errors**
After switching to a non-root user, the app failed to access the working directory because ownership wasn't transferred before the `USER` directive.

> **Fix:** Created user and group first, ran `chown -R` on `/app`, then applied `USER` after the file copy step.

---

## Docker Compose Setup

```yaml
Services:
  flask   → Built from Dockerfile, port 8000, env vars, depends_on: mysql (healthy)
  mysql   → mysql:8.0, env vars, healthcheck, named volume, restart policy

Infrastructure:
  Network → Custom bridge network
  Volume  → Named volume for DB persistence
```

Key features implemented:

- Custom network for service isolation
- Named volume for database persistence
- MySQL healthcheck with `mysqladmin ping`
- `depends_on` with `condition: service_healthy`
- Restart policy on both services
- Environment variable configuration for credentials

---

## Database Resilience

`depends_on: service_healthy` confirms that MySQL passed its healthcheck — but it does **not** guarantee the database is ready to accept connections. The Flask app handles this with retry logic:

- Attempts connection multiple times on startup
- Sleeps between retries
- Fails cleanly with a clear error if the database stays unreachable

This prevents crash loops and reflects how real microservices handle readiness in distributed environments.

---

## Image Size Comparison

| Image | Size |
|---|---|
| `python:3.11-slim` | ~167 MB |
| `gcr.io/distroless/python3-debian12` | ~74.8 MB |
| **Reduction** | **~92 MB (~55%)** |

The difference comes from distroless stripping all non-essential Linux distribution components — only the minimal Python runtime is included.

---

## Docker Hub

The optimized distroless image is publicly available:

```bash
docker pull heyyprakhar1/distroless-image
```

---

## Cold Start Test

To validate the full stack end-to-end:

1. Removed all containers and images
2. Pulled the image fresh from Docker Hub
3. Started the stack with Docker Compose
4. Verified: DB starts → healthcheck passes → Flask connects → app works in browser

The stack runs cleanly from scratch.

---

## Key Learnings

1. Multi-stage builds reduce image size significantly — distroless cuts it by ~55%
2. Distroless images improve security posture but require planning for debugging
3. Non-root containers are essential for production; get the `chown` order right
4. Healthchecks confirm liveness, not application readiness — retry logic fills the gap
5. Docker layer caching must be handled deliberately to avoid stale builds
6. Cold-start tests are the only real proof that everything works end-to-end

---

## Final Status

| Task | Status |
|---|---|
| Multi-stage build | ✅ |
| Non-root user configured | ✅ |
| Healthchecks added | ✅ |
| Custom network created | ✅ |
| Volume for persistence added | ✅ |
| Image optimized (~55% smaller) | ✅ |
| Image pushed to Docker Hub | ✅ |
| Full cold-start test passed | ✅ |

---

> Built. Broke. Debugged. Optimized. Shipped. This is exactly what happens in real DevOps environments.