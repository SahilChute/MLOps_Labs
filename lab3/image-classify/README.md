# 🐳 Dockerized Image Classifier — PyTorch + FastAPI + Redis

A REST API that classifies images using a pre-trained ResNet50 model, served with FastAPI and cached with Redis. Fully containerized with Docker and Docker Compose.

---

## Prerequisites

Make sure you have the following installed:
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/) (included with Docker Desktop)

---

## Project Structure

```
image-classifier/
├── app/
│   ├── main.py           # FastAPI app with Redis caching
│   └── model.py          # ResNet50 model loading & inference
├── Dockerfile            # Container definition
├── requirements.txt      # Python dependencies
└── docker-compose.yml    # Multi-container setup (API + Redis)
```

---

## Running the App

### 1. Clone the repository
```bash
git clone <repo-url>
cd lab3/image-classifier
```

### 2. Start all containers with Docker Compose
```bash
docker-compose up --build
```

This will:
- Build the API image from the Dockerfile
- Pull the official Redis image
- Start both containers

Wait until you see:
```
api_1    | INFO:     Application startup complete.
```

---

## Testing the API

### Option 1 — Swagger UI (Recommended)
Open your browser and go to:
```
http://localhost:8000/docs
```
1. Click **POST /predict**
2. Click **Try it out**
3. Upload any image file (have uploaded test images in lab3/testImages)
4. Click **Execute**
5. View predictions in the response body

### Option 2 — curl
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@/path/to/your/image.jpg"
```

### Health Check
```bash
curl http://localhost:8000/health
```

---

## Example Response

**First request** (model runs inference):
```json
{
  "filename": "dog.jpg",
  "predictions": [
    {"label": "golden retriever", "confidence": 0.8921},
    {"label": "Labrador retriever", "confidence": 0.0432},
    {"label": "cocker spaniel", "confidence": 0.0201},
    {"label": "tennis ball", "confidence": 0.0098},
    {"label": "Irish setter", "confidence": 0.0071}
  ],
  "cached": false
}
```

**Same image again** (served from Redis cache):
```json
{
  "filename": "dog.jpg",
  "predictions": [...],
  "cached": true
}
```

---

## Stopping the App

```bash
docker-compose down
```

To also remove the Redis volume (clears cached predictions):
```bash
docker-compose down -v
```
