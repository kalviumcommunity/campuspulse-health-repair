# Restore Trustworthy Health Reporting

CampusPulse API starts, but its container probe fails and readiness reports success even when inventory is unavailable. Repair health reporting and demonstrate truthful dependency failure detection and recovery.

**Starter repository:** https://github.com/kalviumcommunity/campuspulse-health-repair  
**Allowed edits:** compose.yaml: only api.healthcheck URL path; readiness.py: readiness function only. Preserve probe timings, helper, app routes, ports and all other files.

## Prerequisites and startup

Use Python 3.10+ on host, Git, Docker Engine/Desktop and Compose v2 (supports --no-log-prefix). Linux/macOS or prepared WSL. No pip packages, jq, paid tools, registry credentials or cloud account required. Docker Desktop subject to its license; free Linux Docker Engine sufficient.

Clone supplied repo (fork optional), enter directory and reserve host port 18091. Build and start:

```sh
docker pull python:3.12-slim
# No additional monitoring image needed.
docker compose config --quiet
docker compose build
mkdir -p evidence
docker compose up -d
```

Wait up to 15 seconds for listeners/probes/scrapes before diagnosing. Initial task faults are intentional, not setup failures. Commands run from repo root. Host evidence/ is ignored. Use a fresh exercise stack with no unrelated traffic. Do not edit helpers to force checks to pass.

## Task 1: Repair container probe

CampusPulse API responds at /health, but Docker marks it unhealthy. Compare the endpoint response with actual probe status/output. Repair only the probe URL path; recreate and wait until healthy. Do not disable the probe or change its timings.

```sh
python3 http_get.py http://localhost:18091/health
docker compose ps
docker compose exec -T api python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz')"
# Inspect actual probe history; this command does not depend on a fixed container name:
docker inspect --format '{{json .State.Health}}' "$(docker compose ps -q api)"
# After permitted repair:
docker compose up -d --build
# Allow up to 15 seconds for probe status, then inspect again.
```


## Task 2: Repair readiness

Stop inventory. Capture original /ready response that incorrectly says ready. Repair readiness(dependency_available) to CALL the supplied Boolean helper: return HTTP 200 with status ready when true, HTTP 503 with status not ready when false. Keep /health shallow and independent. Rebuild API while inventory remains stopped (use --no-deps); prove /health=200 and /ready=503.

```sh
docker compose stop inventory
python3 http_get.py http://localhost:18091/ready
# After readiness.py repair; do not restart inventory yet:
docker compose up -d --build --no-deps api
python3 http_get.py http://localhost:18091/health
python3 http_get.py http://localhost:18091/ready
```


## Task 3: Verify recovery and explain

Restore inventory without editing its implementation. Show /ready changes from 503 to 200 and /health remains 200; show API healthy. Write two findings: (1) process running/liveness versus readiness, supported by observed responses; (2) why Docker health status alone neither restarts an unhealthy running process nor routes traffic away. The container probe here checks liveness, so API can remain Docker-healthy during inventory outage.

```sh
docker compose start inventory
# Allow up to 5 seconds for dependency listener startup.
python3 http_get.py http://localhost:18091/health
python3 http_get.py http://localhost:18091/ready
docker compose ps
```


## Cleanup

```sh
docker compose down
```

Remove only resources created for this exercise. Preserve supplied fixtures and helpers; do not bypass checks or fabricate results.
