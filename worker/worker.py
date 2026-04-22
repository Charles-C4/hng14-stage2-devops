import redis
import time
import os
import signal


# Use environment variable with fallback for local dev
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Graceful shutdown flag
running = True


def signal_handler(signum, frame):
    global running
    print(f"Received signal {signum}, shutting down gracefully...")
    running = False


# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def process_job(job_id):
    print(f"Processing job {job_id}")
    try:
        time.sleep(2)  # simulate work
        r.hset(f"job:{job_id}", "status", "completed")
        print(f"Done: {job_id}")
    except Exception as e:
        print(f"Error processing job {job_id}: {e}")
        r.hset(f"job:{job_id}", "status", "failed")


print("Worker started, waiting for jobs...")

while running:
    try:
        job = r.brpop("job", timeout=5)

        if job:
            _, job_id = job
            process_job(job_id)

    except redis.ConnectionError as e:
        print(f"Redis connection error: {e}, retrying in 5 seconds...")
        time.sleep(5)

    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(1)

print("Worker stopped.")
