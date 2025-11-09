# Apache Superset 6.0.0 — Portainer-ready

This stack deploys Superset with Postgres + Redis + Celery (worker/beat), optional Alerts & Reports, and a custom image with many database drivers pre-installed.

## 1) Prerequisites
- Docker + Portainer (v2.19+ recommended)
- Host ports 8088 (HTTP), and storage space for volumes

## 2) Clone and configure
```bash
git clone <your-repo-url> superset-stack
cd superset-stack
cp .env.example .env
# Edit .env and set strong SUPERSET_SECRET_KEY, Postgres credentials, etc.
```

Optionally adjust `superset/superset_config.py` and the driver sets in `superset-build/requirements-drivers.txt`.

## 3) Build the custom image (recommended)

In Portainer **or** CLI:

```bash
# CLI path
docker compose --profile build build superset-build
```

Portainer path: **Images → Build a new image** (or Stack build). Use build context `./superset-build`, Dockerfile `Dockerfile`, and ARG `SUPERSET_TAG=6.0.0`.

## 4) Deploy via Portainer (Stacks)

1. Open **Portainer → Stacks → Add stack**.
2. Name it (e.g., `superset6`).
3. Paste the entire `docker-compose.yml` into the Web editor **or** upload from a Git repo.
4. Click **Deploy the stack**.

Portainer will create the stack and start **postgres**, **redis**, and **superset** services.

## 5) Initialize Superset

Run the one-shot init job **once** (Portainer UI or CLI):

```bash
docker compose run --rm init
```

This applies DB migrations and creates the admin user defined in `.env`.

## 6) Start workers

Make sure the app and workers are up:

```bash
docker compose up -d superset worker beat
# Optional for Alerts & Reports (screenshots)
docker compose up -d worker_reports
```

## 7) Login

Open `http://<your-host>:8088` and log in with the admin credentials from `.env`.

## 8) Add databases and datasets

* Install any additional drivers (already baked by the custom image; or drop extra ones into `docker/requirements-local.txt`).
* Add database connections in **Settings → Data → Database Connections**.
* To bulk-import, put `assets/datasources.zip` or a `assets/datasources/` folder and run:

```bash
docker compose run --rm import_datasources
```

## 9) Production tips

* Put Superset behind a reverse proxy (Traefik/Nginx) for TLS.
* Set a strong `SUPERSET_SECRET_KEY` and rotate credentials.
* Backup the Postgres volume regularly.
* Pin `SUPERSET_TAG` and upgrade deliberately: change the tag → pull → `docker compose up -d` → re-run `init`.

## Troubleshooting

* **Driver missing**: add to `superset-build/requirements-drivers.txt` and rebuild, or to `docker/requirements-local.txt`.
* **SQL Server (pyodbc)**: ensure MS ODBC 18 is installed (see commented lines in Dockerfile).
* **Alerts/Reports screenshots**: keep `worker_reports` running; Playwright Chromium is pre-installed.

## Persistent Volumes (Synology NAS)

Which data to persist
- `superset_db` → Postgres metadata (dashboards, charts, users). Container path: `/var/lib/postgresql/data`.
- `superset_home` → Superset home (uploads, thumbnails, logs). Container path: `/app/superset_home`.
- `pythonpath` (optional) → Custom config. Place `superset_config.py` here. Container path: `/app/pythonpath`.
- Redis is ephemeral by default here. Persist only if you need durable cache/results.

Default behavior
- The compose uses named volumes (`superset_db`, `superset_home`), which Docker stores on the host. This is fine for most setups.

Bind-mount to a Synology shared folder
1) Create shared folders in DSM, e.g. `/volume1/docker/superset/postgres`, `/volume1/docker/superset/home`, and `/volume1/docker/superset/pythonpath`.
2) Ensure the user that runs Docker/Portainer has read/write permissions to these folders.
3) Replace the named volumes with bind mounts in your stack:

```yaml
services:
  postgres:
    volumes:
      - /volume1/docker/superset/postgres:/var/lib/postgresql/data

  superset:
    volumes:
      - /volume1/docker/superset/home:/app/superset_home
      - /volume1/docker/superset/pythonpath:/app/pythonpath:ro
    environment:
      SUPERSET_CONFIG_PATH: /app/pythonpath/superset_config.py
```

Optional: Persist Redis
- Remove the in-memory flags and mount `/data`:

```yaml
services:
  redis:
    command: ["redis-server"]
    volumes:
      - /volume1/docker/superset/redis:/data
```

Notes
- The previously declared `local_docker_dir` volume is not used; it can be removed safely.
- Copy your config file into `/volume1/docker/superset/pythonpath/superset_config.py` (you can use the sample in `superset/superset_config.py` from this repo as a starting point).
- If deploying via Portainer Stacks, edit the stack → update the `volumes:` entries with your Synology paths → Redeploy.
