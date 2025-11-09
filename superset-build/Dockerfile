# Build an image with MANY DB drivers (Superset)
ARG SUPERSET_TAG=latest
FROM apache/superset:${SUPERSET_TAG}

USER root

# System deps for common drivers (mssql/odbc, hive/impala SASL/kerberos, mysqlclient, etc.)
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential gcc g++ make git curl ca-certificates \
    libpq-dev default-libmysqlclient-dev \
    unixodbc unixodbc-dev \
    libsasl2-dev libkrb5-dev \
    libldap2-dev libssl-dev libffi-dev \
    python3-dev \
  && rm -rf /var/lib/apt/lists/*

# OPTIONAL: MS ODBC driver for pyodbc + SQL Server (uncomment to enable)
# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#  && curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#  && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Copy requirements first for better caching
COPY requirements-drivers.txt /tmp/requirements-drivers.txt

# Use the virtualenv in the base image and install drivers with uv
RUN . /app/.venv/bin/activate \
 && uv pip install --upgrade pip \
 && uv pip install -r /tmp/requirements-drivers.txt \
 && uv pip install openpyxl Pillow \
 && uv pip install playwright \
 && playwright install-deps \
 && PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/playwright-browsers playwright install chromium || true

USER superset
