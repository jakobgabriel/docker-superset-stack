# Apache Superset — Light Docker Compose

This repository is aligned with the official “light” docker-compose from the Apache Superset project. It runs only the essentials: a Postgres metadata DB and the Superset app, with optional frontend dev server and a pytest runner profile. Redis, Celery workers, and other heavy services are intentionally excluded.

References
- Upstream light compose: https://github.com/apache/superset/blob/master/docker-compose-light.yml
- Superset docs: https://superset.apache.org/docs/installation/docker-compose

What’s included here
- docker-compose.simple.yml — copied from upstream “light” compose
- docker/.env — default environment used by services
- docker/docker-bootstrap.sh, docker/docker-init.sh — app bootstrap and init scripts
- docker/docker-frontend.sh — starts the webpack dev server (optional)
- docker/docker-pytest-entrypoint.sh — pytest profile entrypoint (optional)
- docker/pythonpath_dev/superset_config_docker_light.py — config that removes Redis and uses SimpleCache

Removed as unnecessary for light setup
- docker-compose.yml (heavy stack with Redis/Celery/workers)
- Root .env files (.env, .env.example, .env.simple)
- superset-build/ (custom image build context)

Prerequisites
- Docker and Docker Compose
- Upstream Superset source tree or required files locally. The light compose builds from the repo root and mounts folders; you need at minimum:
  - Dockerfile (multi-stage) compatible with Superset
  - superset/ (backend source)
  - superset-frontend/ (frontend source; required if using superset-node-light)
  - docker/ (provided here) and tests/ (only for pytest profile)

Quick start
1) Ensure required files/folders are present (clone the upstream repo or place them here).
2) Start DB and initialize Superset:
   - docker compose -f docker-compose.simple.yml up db-light superset-init-light
3) Start the app:
   - docker compose -f docker-compose.simple.yml up superset-light
4) Optional: start the frontend dev server (hot-reload):
   - docker compose -f docker-compose.simple.yml up superset-node-light
5) Access the UI:
   - http://localhost:${NODE_PORT:-9001}

Environment configuration
- Default variables are in docker/.env
- Local overrides (optional): create docker/.env-local — compose will load it if present
- Set SUPERSET_LOAD_EXAMPLES=yes to load example dashboards during init

Volumes
- Named volumes store app state:
  - superset_home_light → /app/superset_home
  - db_home_light → /var/lib/postgresql/data

Notes
- This setup mirrors the upstream “light” experience. If you need the full stack with Redis, Celery workers, Alerts & Reports, use the official docker-compose.yml from the upstream repo instead.
- If you prefer a single-container image-based setup (without building from source), ask and we can add an alternative compose alongside this light template.
