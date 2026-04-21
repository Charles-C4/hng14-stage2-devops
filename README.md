# hng14-stage2-devops

A containerized job processing system with three microservices:

- **Frontend** (Node.js/Express) — User interface for submitting and tracking jobs
- **API** (Python/FastAPI) — Creates jobs and serves status updates
- **Worker** (Python) — Processes jobs from Redis queue
- **Redis** — Message queue and state storage

## Prerequisites

| Tool | Version |
|------|---------|
| Docker | 24.0+ |
| Docker Compose | 2.20+ |
| Git | 2.0+ |

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hng14-stage2-devops.git
cd hng14-stage2-devops
```
### 2. Start the stack 

```bash 
docker-compose up --build
```
### 3. Access the application

```bash 
Open http://localhost:3000 

``` 
### 4. Test the system 

 1. Click "Submit New Job"
 2. Watch the status change from "queued"➡️ "completed"
 3. Job Processing takes ~ 2 seconds 
 
