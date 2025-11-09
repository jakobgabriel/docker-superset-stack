# Superset 6.0.0 config (safe defaults). Adjust to your environment.
import os
from flask_caching.backends.rediscache import RedisCache

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")

# Redis-backed cache & results backend
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "HOST": "redis",
    "PORT": 6379,
    "DB": 1,
}
RESULTS_BACKEND = RedisCache(host="redis", port=6379, key_prefix="superset_results")
RESULTS_BACKEND_USE_MSGPACK = True

# Celery configuration for async queries
class CeleryConfig:
    broker_url = "redis://redis:6379/0"
    result_backend = "redis://redis:6379/0"
    imports = ("superset.sql_lab", "superset.tasks.scheduler")
    worker_prefetch_multiplier = 10
    task_acks_late = True

CELERY_CONFIG = CeleryConfig

FEATURE_FLAGS = {
    "ALERT_REPORTS": False,  # flip to True if you start worker_reports
    "EMBEDDED_SUPERSET": True,
}

# Optional: Mapbox
MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY", "")

# Security hardening
WTF_CSRF_ENABLED = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

