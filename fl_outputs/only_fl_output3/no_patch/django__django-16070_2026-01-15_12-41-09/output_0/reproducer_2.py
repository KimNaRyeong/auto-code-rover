# reproducer.py
import os
import django
from django.core.exceptions import FieldError
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

def setup_django_environment():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    SECRET_KEY = 'fake-key'
    INSTALLED_APPS = (
        '__main__',
    )
    django.setup()

setup_django_environment()

class RelatedModel(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        app_label = __name__

class SomeModel(models.Model):
    some_foreign_key = models.ForeignKey(RelatedModel, on_delete=models.CASCADE)
    
    class Meta:
        app_label = __name__

try:
    # Attempt to order by a non-existing field in a related model.
    # This is expected to raise a FieldError if the issue is fixed.
    SomeModel.objects.all().order_by("some_foreign_key__non_existing_field")
    print("Issue detected: Ordering by a non-existing field in a related model did not raise FieldError.")
    raise AssertionError("Did not raise FieldError for non-existing related field. The issue is still present.")
except FieldError:
    print("Correctly threw FieldError for a non-existing field in a related model. The issue appears to be fixed.")
    os._exit(0)
except Exception as e:
    print_stacktrace(e)
    os._exit(1)
