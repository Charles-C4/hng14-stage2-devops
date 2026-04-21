# FIXES.md — Application Bug Fixes

## Overview
Documenting all bugs found and fixes applied to make the application production-ready.

---

## 1. api/main.py

### Issue 1: Hardcoded Redis Host
- **File:** `api/main.py`
- **Line:** 7
- **Problem:** `r = redis.Redis(host="localhost", port=6379)` hardcodes localhost
- **Fix:** Changed to use environment variable: `REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")`

### Issue 2: No Health Endpoint
- **File:** `api/main.py`
- **Line:** N/A (missing)
- **Problem:** No health check endpoint for container healthchecks
- **Fix:** Added `/health` endpoint that pings Redis

### Issue 3: No Error Handling
- **File:** `api/main.py`
- **Lines:** 12-20
- **Problem:** Redis operations have no try/catch, failures crash the app
- **Fix:** Wrapped all Redis operations in try/except blocks

### Issue 4: No Logging
- **File:** `api/main.py`
- **Problem:** No visibility into application behavior
- **Fix:** Added print statements for job creation and errors

---

## 2. worker/worker.py

### Issue 1: Hardcoded Redis Host
- **File:** `worker/worker.py`
- **Line:** 5
- **Problem:** `r = redis.Redis(host="localhost", port=6379)` hardcodes localhost
- **Fix:** Changed to use environment variable: `REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")`

### Issue 2: No Graceful Shutdown
- **File:** `worker/worker.py`
- **Problem:** Worker doesn't handle SIGTERM, causes hard container stops
- **Fix:** Added signal handlers for SIGTERM/SIGINT with graceful shutdown flag

### Issue 3: No Error Handling
- **File:** `worker/worker.py`
- **Lines:** 14-22
- **Problem:** No try/catch around job processing or Redis connection
- **Fix:** Added try/except in process_job() and main loop

### Issue 4: No Connection Retry
- **File:** `worker/worker.py`
- **Problem:** Worker crashes if Redis is temporarily unavailable
- **Fix:** Added retry logic with 5-second sleep on connection errors

---

## 3. frontend/app.js

### Issue 1: Hardcoded API URL
- **File:** `frontend/app.js`
- **Line:** 6
- **Problem:** `const API_URL = "http://localhost:8000"` won't work in Docker
- **Fix:** Changed to `const API_URL = process.env.API_URL || "http://localhost:8000"`

### Issue 2: Hardcoded Port
- **File:** `frontend/app.js`
- **Line:** 27
- **Problem:** Port 3000 is hardcoded
- **Fix:** Changed to use `process.env.PORT || 3000`

---

## 4. frontend/views/index.html

### Issue 1: No Error Handling in submitJob()
- **File:** `frontend/views/index.html`
- **Line:** 27
- **Problem:** fetch() has no try/catch, errors are unhandled
- **Fix:** Added try/catch with error display to user

### Issue 2: No Error Handling in pollJob()
- **File:** `frontend/views/index.html`
- **Line:** 34
- **Problem:** Polling errors are silently ignored
- **Fix:** Added try/catch, shows 'error' status on failure

---

## 5. Security: Exposed .env File (CRITICAL)

### Issue: Secrets Committed to Git
- **File:** `api/.env`
- **Problem:** `.env` file with `REDIS_PASSWORD=supersecretpassword123` was committed to git history
- **Impact:** SECURITY BREACH - credentials exposed in version control
- **Fix:** Remove the file from git and ensure .gitignore is respected

---

## Summary

| File | Issues Found | Issues Fixed |
|------|--------------|--------------|
| api/main.py | 4 | 4 |
| worker/worker.py | 4 | 4 |
| frontend/app.js | 2 | 2 |
| frontend/views/index.html | 2 | 2 |
| api/.env | 1 (SECURITY) | 1 |
| **Total** | **13** | **13** |
| **Total** | **12** | **12** |
