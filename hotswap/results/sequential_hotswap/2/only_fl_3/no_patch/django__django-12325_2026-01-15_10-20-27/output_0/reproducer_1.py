"""
reproducer.py: Script to reproduce the reported Django model inheritance issue.
"""

import os
import sys
import django
from django.conf import settings
from django.db import models
from django.core.exceptions import ImproperlyConfigured

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Django environment setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    },
    INSTALLED_APPS=[
        "__main__",  # Hack to allow Django to recognize this script as an app
    ],
    SECRET_KEY="not_very_secret_in_this_case",
    TIME_ZONE="UTC",
    USE_TZ=True,
)

django.setup()

class Document(models.Model):
    pass

try:
    class Picking(models.Model):
        document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
        origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)

    class PickingFixed(models.Model):
        origin = models.OneToOneField(Document, related_name='picking_fixed', on_delete=models.PROTECT)
        document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')

    assert False, "ImproperlyConfigured error was expected but not raised."
except ImproperlyConfigured as e:
    print("Expected error was caught. Test reproduces the issue successfully.")
    print_stacktrace(e)
    sys.exit(0)
except Exception as e:
    print("An unexpected error occurred.", file=sys.stderr)
    print_stacktrace(e)
    assert False, "Test failed due to an unexpected error."
