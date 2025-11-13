import os
from django.conf import settings
from django.db import models

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

settings.configure()
settings.LOCAL_FILE_DIR = '/tmp'

try:
    class LocalFiles(models.Model):
        name = models.CharField(max_length=255)
        file = models.FilePathField(path=lambda: os.path.join(settings.LOCAL_FILE_DIR, 'example_dir'))
    
    print("Creating model...")
    LocalFiles()
    print("Model created successfully!")
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present: FilePathField path does not accept a callable.")
