"""Customer file uploads (return labels, damage photos)."""

import os

UPLOAD_ROOT = "/var/app/uploads"
MAX_BYTES = 10 * 1024 * 1024


def save_upload(customer_id, filename, data):
    """Store an uploaded file under the customer's folder."""
    if len(data) > MAX_BYTES:
        raise ValueError("file too large")
    folder = os.path.join(UPLOAD_ROOT, str(customer_id))
    os.makedirs(folder, exist_ok=True)
    destination = os.path.join(folder, filename)
    with open(destination, "wb") as f:
        f.write(data)
    return destination
