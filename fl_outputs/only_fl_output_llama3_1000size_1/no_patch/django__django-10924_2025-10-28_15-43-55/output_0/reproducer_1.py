import os
from django.conf import settings
from django.core.exceptions import AssertionError
from django.db import models
from django.core.exceptions import ImproperlyConfigured

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    settings.LOCAL_FILE_DIR
except ImproperlyConfigured as e:
    print_stacktrace(e)
    exit(1)
else:
    assert not os.path.exists(os.path.join(settings.LOCAL_FILE_DIR, 'example_dir'))
    exit(0)
