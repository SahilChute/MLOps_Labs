from flask import Flask, request, jsonify, send_file
from google.cloud import storage
from PIL import Image, ImageFilter
import os
import io

app = Flask(__name__)

BUCKET_NAME = os.environ.get('BUCKET_NAME')
BLUR_RADIUS = int(os.environ.get('BLUR_RADIUS', 10))  # default blur strength
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_storage_client():
    return storage.Client()


# ── Health check ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return jsonify({
        "status": "Image blur service is running",
        "blur_radius": BLUR_RADIUS,
        "endpoints": {
            "POST /blur":                "Upload and blur one or more images",
            "GET  /download/<filename>": "Download a blurred image",
            "GET  /list":                "List all blurred images in the bucket"
        }
    }), 200


# ── BLUR (batch upload + process + save) ────────────────────────────────────
@app.route('/blur', methods=['POST'])
def blur_images():
    """
    Accept multiple image files, blur each one, and save to GCS.
    Usage: POST /blur with form-data field 'images' (repeat for multiple files)
    """
    if not BUCKET_NAME:
        return jsonify({"error": "BUCKET_NAME env var not set"}), 500

    files = request.files.getlist('images')
    if not files or all(f.filename == '' for f in files):
        return jsonify({"error": "No files provided. Use field name 'images'."}), 400

    client = get_storage_client()
    bucket = client.bucket(BUCKET_NAME)

    results = []
    for file in files:
        if not allowed_file(file.filename):
            results.append({
                "file": file.filename,
                "status": "skipped",
                "reason": f"Unsupported file type. Allowed: {ALLOWED_EXTENSIONS}"
            })
            continue

        try:
            # ── Extract: read uploaded image into memory
            # img = Image.open(file.stream).convert("RGB")
            file.stream.seek(0)
            img_bytes = io.BytesIO(file.stream.read())
            img = Image.open(img_bytes).convert("RGB")
            original_size = img.size

            # ── Transform: save original, then apply Gaussian blur
            orig_blob = bucket.blob(f"originals/{file.filename}")
            orig_buffer = io.BytesIO()
            img.save(orig_buffer, format="JPEG")
            orig_buffer.seek(0)
            orig_blob.upload_from_file(orig_buffer, content_type="image/jpeg")

            blurred_img = img.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))

            # ── Load: save blurred image to GCS under blurred/
            blurred_filename = f"blurred_{file.filename}"
            blurred_blob = bucket.blob(f"blurred/{blurred_filename}")
            blurred_buffer = io.BytesIO()
            blurred_img.save(blurred_buffer, format="JPEG")
            blurred_buffer.seek(0)
            blurred_blob.upload_from_file(blurred_buffer, content_type="image/jpeg")

            results.append({
                "file": file.filename,
                "status": "success",
                "original_size": original_size,
                "blur_radius": BLUR_RADIUS,
                "saved_as": blurred_filename,
                "download_url": f"/download/{blurred_filename}"
            })

        except Exception as e:
            results.append({
                "file": file.filename,
                "status": "error",
                "reason": str(e)
            })

    success_count = sum(1 for r in results if r["status"] == "success")
    return jsonify({
        "total_received": len(files),
        "total_blurred":  success_count,
        "results": results
    }), 200


# ── DOWNLOAD ─────────────────────────────────────────────────────────────────
@app.route('/download/<filename>')
def download_image(filename):
    """Download a blurred image by filename."""
    if not BUCKET_NAME:
        return jsonify({"error": "BUCKET_NAME env var not set"}), 500

    try:
        client = get_storage_client()
        bucket = client.bucket(BUCKET_NAME)
        blob   = bucket.blob(f"blurred/{filename}")

        image_data = blob.download_as_bytes()
        return send_file(
            io.BytesIO(image_data),
            mimetype='image/jpeg',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"error": f"File not found: {filename}", "details": str(e)}), 404


# ── LIST ─────────────────────────────────────────────────────────────────────
@app.route('/list')
def list_blurred():
    """List all blurred images currently stored in the bucket."""
    if not BUCKET_NAME:
        return jsonify({"error": "BUCKET_NAME env var not set"}), 500

    client = get_storage_client()
    bucket = client.bucket(BUCKET_NAME)
    blobs  = client.list_blobs(BUCKET_NAME, prefix="blurred/")

    files = []
    for blob in blobs:
        filename = blob.name.replace("blurred/", "")
        if filename:
            files.append({
                "filename":     filename,
                "size_bytes":   blob.size,
                "updated":      blob.updated.isoformat(),
                "download_url": f"/download/{filename}"
            })

    return jsonify({
        "total_blurred_images": len(files),
        "images": files
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)