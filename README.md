# Q1: Restore Trustworthy Health Reporting

**Course:** DevOps Foundation · **Module:** 5, Monitoring, Cost & Production Readiness  
**Submission:** one PDF file upload · **Difficulty:** medium · **Marks:** 20  
**Target duration:** 32 minutes, including screenshots and PDF assembly after preparation. Budget 40 minutes maximum; pilot timing not yet measured.  
**Lesson alignment:** 5.1 signals; 5.2 health checks.

## Problem statement

CampusPulse API starts, but its container probe fails and readiness reports success even when inventory is unavailable. Repair health reporting and demonstrate truthful dependency failure detection and recovery.

**Starter repository:** https://github.com/kalviumcommunity/campuspulse-health-repair  
**Allowed edits:** compose.yaml: only api.healthcheck URL path; readiness.py: readiness function only. Preserve probe timings, helper, app routes, ports and all other files.

## Preparation (before assessment timer)

Use Python 3.10+ on host, Git, Docker Engine/Desktop and Compose v2 (supports --no-log-prefix). Linux/macOS or prepared WSL. No pip packages, jq, paid tools, registry credentials or cloud account required. Docker Desktop subject to its license; free Linux Docker Engine sufficient.

Clone supplied repo (fork optional), enter directory and reserve host port 18091. Download/build before timer:

```sh
docker pull python:3.12-slim
# No additional monitoring image needed.
docker compose config --quiet
docker compose build
mkdir -p evidence
docker compose up -d
```

Wait up to 15 seconds for listeners/probes/scrapes before diagnosing. Initial task faults are intentional, not setup failures. If Docker/tool/download or port setup fails, resolve before starting timer. Commands run from repo root. Host evidence/ is ignored. Use a fresh exercise stack with no unrelated traffic. Do not edit helpers to force checks to pass.

## Task 1: Repair container probe (6 marks, ~9 minutes)

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

**Evidence:** capture actual commands/results requested above and add a short cause/fix/result caption. Extra screenshots are allowed when output cannot fit readably. At least one labelled screenshot per task; one screenshot need not contain all checks.

## Task 2: Repair readiness (7 marks, ~13 minutes)

Stop inventory. Capture original /ready response that incorrectly says ready. Repair readiness(dependency_available) to CALL the supplied Boolean helper: return HTTP 200 with status ready when true, HTTP 503 with status not ready when false. Keep /health shallow and independent. Rebuild API while inventory remains stopped (use --no-deps); prove /health=200 and /ready=503.

```sh
docker compose stop inventory
python3 http_get.py http://localhost:18091/ready
# After readiness.py repair; do not restart inventory yet:
docker compose up -d --build --no-deps api
python3 http_get.py http://localhost:18091/health
python3 http_get.py http://localhost:18091/ready
```

**Evidence:** capture actual commands/results requested above and add a short cause/fix/result caption. Extra screenshots are allowed when output cannot fit readably. At least one labelled screenshot per task; one screenshot need not contain all checks.

## Task 3: Verify recovery and explain (7 marks, ~10 minutes)

Restore inventory without editing its implementation. Show /ready changes from 503 to 200 and /health remains 200; show API healthy. Write two findings: (1) process running/liveness versus readiness, supported by observed responses; (2) why Docker health status alone neither restarts an unhealthy running process nor routes traffic away. The container probe here checks liveness, so API can remain Docker-healthy during inventory outage.

```sh
docker compose start inventory
# Allow up to 5 seconds for dependency listener startup.
python3 http_get.py http://localhost:18091/health
python3 http_get.py http://localhost:18091/ready
docker compose ps
```

**Evidence:** capture actual commands/results requested above and add a short cause/fix/result caption. Extra screenshots are allowed when output cannot fit readably. At least one labelled screenshot per task; one screenshot need not contain all checks.

## Submission: one PDF only

Three labelled task sections with readable genuine terminal screenshots, requested written findings, and complete diff of permitted files once. No PR, video, ZIP or separate code upload. Retain evidence locally; only PDF is uploaded. Tool choice for PDF assembly is unrestricted; export/print labelled screenshots and text to PDF. Do not expose secrets or personal data. No separate marks for filename, URLs, fork ownership, branch labels or submission commit IDs. An instructor standalone reference is valid under identical technical criteria.

The scored work is exactly the three tasks above. No hidden rubric requirements, duplicate deductions or automatic whole-submission zero for an unrelated missing item. Technical request IDs and release values requested within tasks ARE evidence, not submission metadata. Score missing technical evidence only against its corresponding subcriterion.

## Evaluation rubric

| Task | Explicit task criteria | Marks |
|---|---|---|
| Task 1 | Diagnosis with health200 versus failed probe (2); correct probe path (2); healthy status after repair (2). | 6 |
| Task 2 | False-ready diagnosis (2); helper-based true/false implementation (3); down-state liveness200/readiness503 evidence (2). | 7 |
| Task 3 | Readiness recovery (2); liveness and healthy status (1); two accurate evidence-based findings (2 each). | 7 |

**Total: 6 + 7 + 7 = 20.** Written alternatives accepted when technically correct and supported by requested evidence. No cloud execution required or credited.

## Cleanup (after evidence capture)

```sh
docker compose down
```

Remove only exercise resources, never unrelated containers or images. Source code, supplied fixtures and helper scripts outside allowed edits must remain unchanged.
