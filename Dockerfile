# Multi-stage Dockerfile: base -> runtime (light) -> ml (full)

FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates curl git && rm -rf /var/lib/apt/lists/*

FROM base AS runtime
COPY requirements_light.txt /app/requirements_light.txt
RUN python3 -m venv /opt/dark8-venv \
    && /opt/dark8-venv/bin/pip install --upgrade pip setuptools wheel \
    && /opt/dark8-venv/bin/pip install -r /app/requirements_light.txt
ENV PATH="/opt/dark8-venv/bin:$PATH"
COPY . /app
EXPOSE 8080 9100
CMD ["python3", "start_dark8_os.py"]

FROM runtime AS ml
COPY requirements.txt /app/requirements.txt
ARG WHEEL_DIR=""
# If a wheel directory is provided at build time, copy wheels and install from them
RUN if [ -n "$WHEEL_DIR" ] && [ -d "$WHEEL_DIR" ]; then \
            mkdir -p /wheels && cp -r "$WHEEL_DIR"/* /wheels/ || true; \
            /opt/dark8-venv/bin/pip install --no-index --find-links /wheels -r /app/requirements.txt || true; \
        else \
            /opt/dark8-venv/bin/pip install -r /app/requirements.txt || true; \
        fi
ENV PATH="/opt/dark8-venv/bin:$PATH"
CMD ["python3", "start_dark8_os.py"]
