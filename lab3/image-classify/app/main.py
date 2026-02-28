from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import io
import hashlib
import json
import redis
import os
from app.model import predict

app = FastAPI(title="Image Classifier API")

# Connect to Redis using the service name "redis" as the host
cache = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379)

def get_image_hash(contents: bytes) -> str:
    """Create a unique hash for each image to use as cache key"""
    return hashlib.md5(contents).hexdigest()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def classify_image(file: UploadFile = File(...), top_k: int = 5):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()
    image_hash = get_image_hash(contents)
    cache_key = f"prediction:{image_hash}:{top_k}"

    # Check if we already have a cached result
    cached = cache.get(cache_key)
    if cached:
        return {
            "filename": file.filename,
            "predictions": json.loads(cached),
            "cached": True        # So you can see when cache is hit
        }

    # Not cached — run the model
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    results = predict(image, top_k=top_k)

    # Store result in Redis for next time
    cache.set(cache_key, json.dumps(results))

    return {
        "filename": file.filename,
        "predictions": results,
        "cached": False
    }