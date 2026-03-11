# Image Blur Service — Cloud Run Lab

A batch image processing pipeline deployed on Google Cloud Run. The service accepts image uploads, applies a Gaussian blur, saves both the original and blurred versions to Google Cloud Storage, and makes them available for download.

**Service URL:** `https://image-blur-service-253172666192.us-central1.run.app`

---
A batch image processing pipeline deployed on Google Cloud Run. The service accepts image uploads, applies a Gaussian blur, saves both the original and blurred versions to Google Cloud Storage, and makes them available for download.
Service URL: https://image-blur-service-253172666192.us-central1.run.app
## Image Constraints

| Constraint | Details |
|---|---|
| Supported formats | `.jpg`, `.jpeg`, `.png`, `.webp` |
| Unsupported formats | `.avif`, `.gif`, `.bmp`, `.tiff` — these will be skipped |
| File naming | Filename extension must match actual file format — renaming `.avif` to `.jpg` without converting will cause an error |
| File size | No limit |
| Image dimensions | No limit |
| Images per request | No limit |

---
## How to Test the Pipeline

### Step 1 — Verify the service is running

Open this URL in your browser:
```
https://image-blur-service-253172666192.us-central1.run.app/
```
Expected response:
```json
{
  "status": "ETL pipeline is running",
  "blur_radius": 10,
  "endpoints": {
    "POST /blur": "Upload and blur one or more images",
    "GET  /download/<filename>": "Download a blurred image",
    "GET  /list": "List all blurred images in the bucket"
  }
}
```

---

### Step 2 — Upload and blur images

Run this command in your terminal with any `.jpg`, `.png`, `.jpeg`, or `.webp` images:
```bash
curl -X POST https://image-blur-service-253172666192.us-central1.run.app/blur \
  -F "images=@images/cat.jpg" \
  -F "images=@images/dog.jpg"
```

If you want to use other images you can paste them in the images directory.

Then blur them:
```bash
curl -X POST https://image-blur-service-253172666192.us-central1.run.app/blur \
  -F "images=@images/test1.jpg" \
  -F "images=@images/test2.jpg"
```

Expected response:
```json
{
  "total_received": 2,
  "total_blurred": 2,
  "results": [
    {
      "file": "test1.jpg",
      "status": "success",
      "original_size": [800, 600],
      "blur_radius": 10,
      "saved_as": "blurred_test1.jpg",
      "download_url": "/download/blurred_test1.jpg"
    },
    ...
  ]
}
```

---

### Step 3 — List all blurred images

Open this in your browser or run via curl:
```
https://image-blur-service-253172666192.us-central1.run.app/list
```

You should see all previously processed images with their filenames, sizes, and download URLs.

---

### Step 4 — Download a blurred image

In your browser, paste:
```
https://image-blur-service-253172666192.us-central1.run.app/download/blurred_test1.jpg
```
The blurred image will download automatically. Open it to visually confirm the blur was applied.

Or via curl:
```bash
curl -OJ https://image-blur-service-253172666192.us-central1.run.app/download/blurred_test1.jpg
```

---

## Infrastructure Overview

| Resource | Details |
|---|---|
| Platform | Google Cloud Run (managed) |
| Region | us-central1 |
| Memory | 512Mi |
| Image Registry | Google Container Registry |
| Storage | Google Cloud Storage (`image-blur-bucket`) |
| Blur Library | Pillow (Gaussian Blur, radius=10) |
| Language | Python / Flask |

**GCS Bucket structure:**
```
image-blur-bucket/
├── originals/    ← original uploaded images
└── blurred/      ← processed blurred images
```
