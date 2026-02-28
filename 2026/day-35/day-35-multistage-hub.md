# Day 35 — Docker Multi-Stage Build & Push to Docker Hub

## 🎯 Objective

Build a **Flask-based DevOps Portfolio** app using a **Multi-Stage Dockerfile** with a **Distroless** final image, then push it to Docker Hub.

---

## 📁 Project Structure

```
day-35/
├── app.py
├── requirements.txt
├── Dockerfile          # Single-stage (dev/reference)
├── Dockerfile.multi    # Multi-stage (production)
└── templates/
    └── index.html
```

---

## 🐍 Application Code

### `app.py`

A simple Flask app with two routes — `/` serves the portfolio page via Jinja2 templating, and `/api/hello` returns a JSON response to test the backend.

### `requirements.txt`

Contains `flask` and `jinja2` as the only dependencies.

### `templates/index.html`

A dark-themed DevOps portfolio page featuring a skills grid (Linux, Docker, AWS, Jenkins, Shell Scripting, Git & GitHub), clickable project cards linking to GitHub repos, and a live `/api/hello` button to test the Flask backend.

---

## 🐳 Stage 1 — Basic Single-Stage Dockerfile

Before moving to multi-stage, a simple Dockerfile was written as a baseline to understand the image size. It uses `python:3.9-slim` as the base, copies the entire project in, installs dependencies via pip globally, and runs `app.py` directly.

This image carries pip, the Python toolchain, and all build-time utilities into production — unnecessary bloat that multi-stage builds eliminate.

---

## 🚀 Stage 2 — Multi-Stage Dockerfile with Distroless

The multi-stage Dockerfile has two clearly defined stages — a `builder` stage using `python:3.9-slim` to install dependencies, and a `runner` stage using `gcr.io/distroless/python3-debian12` as the final, minimal production image.

### Why Distroless?

`gcr.io/distroless/python3-debian12` is a Google-maintained image that contains **only the Python runtime** — no shell, no package manager, no OS utilities.

| Property | `python:3.9-slim` | Distroless |
|---|---|---|
| Shell (`/bin/sh`) | ✅ Present | ❌ Absent |
| pip / apt | ✅ Present | ❌ Absent |
| Attack surface | Higher | Minimal |
| Image size | ~130 MB | ~55 MB |

### How the Stages Work

**Stage 1 (`builder`)** uses `python:3.9-slim` to install all dependencies into an isolated directory `/app/deps` via `pip install --target`. This keeps packages self-contained and portable across stages.

**Stage 2 (`runner`)** starts completely fresh from the Distroless image and copies only what is needed at runtime — the installed packages from `/app/deps`, the `app.py` entrypoint, and the `templates/` folder. Nothing else makes it into the final image — no pip, no shell, no extra source files.

`ENV PYTHONPATH=/app/deps` tells the Distroless Python runtime where to find the installed packages since there is no pip to manage paths automatically.

`CMD ["app.py"]` works without explicitly writing `python` because Distroless sets the Python binary as its default entrypoint.

---

## 🔨 Build the Multi-Stage Image

The image is built using `docker build` with the `-f` flag pointing to the multi-stage Dockerfile and tagged as `portfolio-app:distroless`. After building, `docker images` confirms the Distroless image is roughly half the size of the single-stage image (~55 MB vs ~130 MB).

---

## ▶️ Run & Test the App

The container is run with port `5000` mapped to the host. Both routes are verified in the browser:

| URL | What You See |
|---|---|
| `http://localhost:5000/` | DevOps Portfolio page |
| `http://localhost:5000/api/hello` | `{"message": "Hello from Flask!"}` |

---

## 📤 Push to Docker Hub

### Step 1 — Login

Authenticate to Docker Hub using `docker login`. Using an **Access Token** (Account Settings → Security → New Access Token) is recommended over a plain password.

### Step 2 — Tag the Image

The image is tagged in the format `<dockerhub-username>/<repo>:<tag>`, giving us `heyyprakhar1/portfolio-app:v1`.

### Step 3 — Push

The tagged image is pushed to Docker Hub with `docker push`.

### Step 4 — Pull & Verify

The image is pulled and run directly from Docker Hub to confirm it works end-to-end outside of the local build environment.

Live on Docker Hub: `https://hub.docker.com/r/heyyprakhar1/portfolio-app`

---

## 🔍 Inspect the Final Image

`docker history` is used to audit every layer in the final image, confirming no hidden build artifacts are present. Attempting to exec a shell inside the Distroless container returns an error — proving the shell is truly absent from the image.

---

## 💡 Key Takeaways

- **Multi-stage builds** keep build-time dependencies completely out of the production image.
- **`pip install --target`** installs packages to a custom directory, making them portable across stages with `COPY --from`.
- **Distroless images** strip the shell, package manager, and OS utilities — drastically reducing the attack surface for production containers.
- **`PYTHONPATH`** bridges the gap between pip's custom install path and the Distroless runtime.
- Every layer in the final image can be audited with `docker history` — there are no hidden build artifacts.

---
