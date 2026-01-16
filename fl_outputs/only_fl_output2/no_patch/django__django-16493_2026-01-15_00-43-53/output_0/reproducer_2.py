"""
reproducer.py: Standalone script to reproduce Django FileField callable storage deconstruction issue.
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__main__')
import django
from django.conf import settings
from django.db import models
from django.core.files.storage import default_storage, FileSystemStorage

# Minimal Django settings sufficient for model definition and manipulation
settings.configure(
    DEBUG=True,
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=['__main__'],
    SECRET_KEY='a-very-secret-key-for-testing',
    USE_TZ=True,
)
django.setup()


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


# Define alternative storage and a callable that returns default_storage
other_storage = FileSystemStorage(location='/media/other')

def get_storage():
    # Always return default_storage to simplify reproduction
    return default_storage

# Define a model utilizing a callable storage
class MyModel(models.Model):
    my_file = models.FileField(storage=get_storage)


def test_file_field_deconstruct():
    """
    Test the deconstruction of a FileField with callable storage to ensure
    the storage parameter is correctly included.
    """
    name, path, args, kwargs = MyModel._meta.get_field('my_file').deconstruct()
    if 'storage' not in kwargs or kwargs['storage'] is not get_storage:
        raise AssertionError("Callable storage not correctly included in deconstruction.")


def main():
    try:
        test_file_field_deconstruct()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue not present. Exiting with code 0.")
        sys.exit(0)


if __name__ == "__main__":
    main()
