# failcheck — self-test suite for agent systems (stdlib only)
# Run: podman run --rm -v /path/to/adapter.py:/adapter.py wallydk24/failcheck run --harness adapter
FROM python:3.12-alpine
COPY failcheck /app/failcheck
WORKDIR /app
ENTRYPOINT ["python3", "-m", "failcheck"]
