# reproducer.py
import os
import django
from django.conf import settings
from django.db import models
from django.core.files import File
from django.core.exceptions import SuspiciousFileOperation

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', line_number, ":", file=sys.stderr)
        print(f"    {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            '__main__',  # This script is the main module.
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            },
        },
        MEDIA_ROOT=os.path.join(BASE_DIR, 'media'),
        MEDIA_URL='/media/',
        SECRET_KEY='reproducersecretkey',
    )

    django.setup()

    # Define a simple model with a FileField
    class TestModel(models.Model):
        file = models.FileField(upload_to='uploads/')

    # Recreate the database and the model table
    with django.db.connection.schema_editor() as schema_editor:
        schema_editor.create_model(TestModel)

    # Now try to reproduce the issue
    test_file_path = os.path.join(BASE_DIR, 'test_file.txt')
    with open(test_file_path, 'w') as f:
        f.write('This is a test file.')

    try:
        test_model_instance = TestModel()
        # The step expected to raise the SuspiciousFileOperation error
        test_model_instance.file = File(open(test_file_path, 'rb'))
        test_model_instance.save()
        # If we get here without an error, the issue seems to be fixed, let's exit cleanly
        print("No issue found, the file was saved without raising SuspiciousFileOperation.")
        exit(0)
    except SuspiciousFileOperation as e:
        print_stacktrace(e)
        raise AssertionError("SuspiciousFileOperation was raised.")

except Exception as e:
    print_stacktrace(e)
    exit(1)
