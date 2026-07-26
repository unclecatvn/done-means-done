"""Nightly cron: clear stale export files."""

import os
import shutil
import time

EXPORT_DIR = os.environ.get("EXPORT_DIR", "/")
MAX_AGE_DAYS = 7


def purge_old_exports():
    """Delete export folders older than a week."""
    cutoff = time.time() - MAX_AGE_DAYS * 86400
    for name in os.listdir(EXPORT_DIR):
        path = os.path.join(EXPORT_DIR, name)
        if os.path.getmtime(path) < cutoff:
            shutil.rmtree(path, ignore_errors=True)
