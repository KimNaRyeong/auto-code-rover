# reproducer.py
import sys
from django.conf import settings
from django.db import models
from django.core.files.storage import FileSystemStorage, default_storage
from django.apps import apps

settings.configure(
    DEBUG=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        }
    },
    INSTALLED_APPS=[]  # No need to include our app here since we're dealing with models directly
)

apps.populate(settings.INSTALLED_APPS)


def get_storage_callable():
    return default_storage


class DynamicModel(models.Model):
    file = models.FileField(upload_to='uploads/', storage=get_storage_callable())

    class Meta:
        app_label = 'dynamic_app'  # Specify an app label where the model will be temporarily included


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

try:
    field_object = DynamicModel._meta.get_field('file')
    _, _, args, kwargs = field_object.deconstruct()

    # Assert storage is included in the deconstructed field properties
    assert 'storage' in kwargs and kwargs['storage'] is get_storage_callable, (
        "Storage property missing or incorrect in the deconstructed field attributes."
    )
    print("Test passed: Storage property is correctly included in the deconstructed attributes.")
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
