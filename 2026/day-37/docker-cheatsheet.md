# Docker Cheat Sheet

## Container Commands

| Command | What it does |
|---|---|
| `docker run -it <image>` | Run container interactively |
| `docker run -d -p 8080:80 <image>` | Run container in detached mode, map ports |
| `docker run --name <name> <image>` | Run container with a custom name |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers (including stopped) |
| `docker stop <container>` | Gracefully stop a container |
| `docker kill <container>` | Force stop a container |
| `docker rm <container>` | Remove a stopped container |
| `docker rm -f <container>` | Force remove a running container |
| `docker exec -it <container> bash` | Open a shell inside a running container |
| `docker logs <container>` | View container logs |
| `docker logs -f <container>` | Follow (tail) container logs |
| `docker inspect <container>` | Get detailed container metadata |
| `docker stats` | Live resource usage for all running containers |

---

## Image Commands

| Command | What it does |
|---|---|
| `docker build -t <name>:<tag> .` | Build image from Dockerfile in current dir |
| `docker build -f <file> -t <name> .` | Build from a specific Dockerfile |
| `docker pull <image>` | Pull image from Docker Hub |
| `docker push <user>/<image>:<tag>` | Push image to Docker Hub |
| `docker tag <image> <user>/<image>:<tag>` | Tag an image for pushing |
| `docker images` | List local images |
| `docker rmi <image>` | Remove an image |
| `docker image inspect <image>` | Inspect image layers and metadata |
| `docker history <image>` | Show image layer history |

---

## Volume Commands

| Command | What it does |
|---|---|
| `docker volume create <name>` | Create a named volume |
| `docker volume ls` | List all volumes |
| `docker volume inspect <name>` | Show volume details and mount path |
| `docker volume rm <name>` | Remove a volume |
| `docker run -v <vol>:/path <image>` | Mount a named volume into a container |
| `docker run -v $(pwd):/path <image>` | Bind mount current directory |

---

## Network Commands

| Command | What it does |
|---|---|
| `docker network create <name>` | Create a custom bridge network |
| `docker network ls` | List all networks |
| `docker network inspect <name>` | Show network details and connected containers |
| `docker network connect <net> <container>` | Connect a running container to a network |
| `docker network disconnect <net> <container>` | Disconnect a container from a network |
| `docker network rm <name>` | Remove a network |
| `docker run --network <name> <image>` | Run container on a specific network |

---

## Compose Commands

| Command | What it does |
|---|---|
| `docker compose up` | Start all services (foreground) |
| `docker compose up -d` | Start all services (detached) |
| `docker compose up --build` | Rebuild images then start |
| `docker compose down` | Stop and remove containers + networks |
| `docker compose down -v` | Same as above + removes named volumes |
| `docker compose ps` | List services and their status |
| `docker compose logs -f` | Follow logs for all services |
| `docker compose logs <service>` | Logs for a specific service |
| `docker compose build` | Build/rebuild service images |
| `docker compose exec <service> bash` | Shell into a running service container |
| `docker compose restart <service>` | Restart a specific service |

---

## Cleanup Commands

| Command | What it does |
|---|---|
| `docker system df` | Show disk usage by images, containers, volumes |
| `docker system prune` | Remove all stopped containers, unused networks, dangling images |
| `docker system prune -a` | Same + removes all unused images (not just dangling) |
| `docker container prune` | Remove all stopped containers |
| `docker image prune` | Remove dangling images |
| `docker image prune -a` | Remove all unused images |
| `docker volume prune` | Remove all unused volumes |
| `docker network prune` | Remove all unused networks |

---

## Dockerfile Instructions

| Instruction | What it does |
|---|---|
| `FROM <image>` | Base image for the build |
| `RUN <command>` | Execute command during build (creates a new layer) |
| `COPY <src> <dest>` | Copy files from host into image |
| `ADD <src> <dest>` | Like COPY but also handles URLs and auto-extracts tarballs |
| `WORKDIR /path` | Set the working directory for subsequent instructions |
| `EXPOSE <port>` | Documents which port the container listens on |
| `ENV KEY=value` | Set environment variable (available at build and runtime) |
| `ARG NAME=default` | Build-time variable (not available at runtime) |
| `VOLUME /path` | Create a mount point (anonymous volume) |
| `USER <user>` | Switch to a non-root user |
| `CMD ["exec", "arg"]` | Default command — overridable at `docker run` |
| `ENTRYPOINT ["exec"]` | Fixed entrypoint — CMD becomes its default arguments |
| `HEALTHCHECK` | Define a command to test container health |

---

## Key Distinctions to Remember

**CMD vs ENTRYPOINT**
- `CMD` is the default command — easily overridden at `docker run`
- `ENTRYPOINT` locks the executable — use CMD to provide default args to it
- Together: `ENTRYPOINT ["python"]` + `CMD ["app.py"]` → run `python app.py`

**COPY vs ADD**
- Prefer `COPY` — it's explicit and predictable
- Use `ADD` only when you need URL fetching or automatic tar extraction

**Named Volume vs Bind Mount**
- Named volume: managed by Docker, persists across container removal
- Bind mount: maps a host path directly — useful for dev, risky in prod

**`docker compose down` vs `docker compose down -v`**
- `down` removes containers and networks
- `down -v` also deletes named volumes — data is gone