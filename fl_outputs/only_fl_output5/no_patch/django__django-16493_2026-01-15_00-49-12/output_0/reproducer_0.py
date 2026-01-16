"""
reproducer.py
"""
import os
import sys

# Configure Django setup
import django
from django.conf import settings
from django.core.management import call_command
from django.core.files.storage import FileSystemStorage, default_storage
from django.db import models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}},
    INSTALLED_APPS=['__main__'],
    MEDIA_ROOT=os.path.join(BASE_DIR, 'media'),
    MEDIA_URL='/media/',
)

django.setup()

# Additional storage for demonstration purposes
other_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'other'))

def get_storage():
    import random
    return random.choice([default_storage, other_storage])

class MyModel(models.Model):
    my_file = models.FileField(storage=get_storage)

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

def check_issue():
    try:
        # Mimic the makemigrations behavior by manually calling deconstruct on the field
        name, path, args, kwargs = MyModel._meta.get_field('my_file').deconstruct()
        # Check if the 'storage' argument is serialized correctly
        assert 'storage' in kwargs, "The 'storage' callable should be included in the deconstructed form."
        print("Issue not present. The 'storage' callable is included in the deconstructed form as expected.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exits with non-zero exit code to indicate the presence of the issue

if __name__ == '__main__':
    check_issue()
    sys.exit(0)  # Exit with code 0 when issue is fixed or not detected
