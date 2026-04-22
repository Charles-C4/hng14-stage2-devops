from fastapi import FastAPI, HTTPException
import redis
import uuid
import os


app = FastAPI()

# Use environment variable with fallback for local dev
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


@app.get("/health")
def health_check():
    """Health endpoint for container healthchecks"""
    try:
        r.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {e}")


@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    try:
        r.lpush("job", job_id)
        r.hset(f"job:{job_id}", "status", "queued")
        print(f"Created job: {job_id}")
        return {"job_id": job_id}
    except Exception as e:
        print(f"Error creating job: {e}")
        raise HTTPException(status_code=500, detail="failed to create job")


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        status = r.hget(f"job:{job_id}", "status")
        if status is None or status == "":
            raise HTTPException(status_code=404, detail="not found")
        return {"job_id": job_id, "status": status}
    except Exception as e:
        print(f"Error getting job: {e}")
        raise HTTPException(status_code=500, detail="failed to get job")
    