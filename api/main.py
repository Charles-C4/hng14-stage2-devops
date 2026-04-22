from fastapi import FastAPI, HTTPException
import redis
import uuid
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration from environment variables
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# Initialize Redis client with socket timeout to prevent hanging
r = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    decode_responses=True,
    socket_connect_timeout=5
)

@app.get("/")
def read_root():
    """Root endpoint for basic connectivity check"""
    return {"message": "HNG Stage 2 API is running", "status": "active"}

@app.get("/health")
def health_check():
    """Resilient health endpoint for Docker healthchecks"""
    try:
        # Check if Redis is reachable
        r.ping()
        return {"status": "healthy", "redis": "connected"}
    except redis.ConnectionError as e:
        logger.error(f"Health check failed: Redis unreachable at {REDIS_HOST}")
        # We return a 503 so the healthcheck accurately reflects the failure
        raise HTTPException(status_code=503, detail="Redis connection failed")
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/jobs")
def create_job():
    """Creates a new background job and adds it to the Redis queue"""
    job_id = str(uuid.uuid4())
    try:
        # Use a pipeline or transaction-like approach
        r.lpush("job", job_id)
        r.hset(f"job:{job_id}", mapping={"status": "queued"})
        logger.info(f"Created job: {job_id}")
        return {"job_id": job_id, "status": "queued"}
    except Exception as e:
        logger.error(f"Error creating job: {e}")
        raise HTTPException(status_code=500, detail="Failed to create job")

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    """Retrieves the status of a specific job"""
    try:
        status = r.hget(f"job:{job_id}", "status")
        if not status:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"job_id": job_id, "status": status}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch job status")