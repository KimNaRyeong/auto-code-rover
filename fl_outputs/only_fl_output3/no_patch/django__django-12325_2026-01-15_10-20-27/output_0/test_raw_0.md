Certainly! Below is a Python script named `reproducer.py`. This script attempts to reproduce the issue described where the order of `OneToOneField` definitions in a Django model subclassing another model with `OneToOneField` causes an `ImproperlyConfigured` exception.

```python
import os
import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

# Setting up Django (Mimicking standalone script environment)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    },
    INSTALLED_APPS=[
        '__main__',  # So Django recognizes this script as an app
    ],
    TIME_ZONE='UTC',
    USE_TZ=True,
)

django.setup()

# Models definition attempt to reproduce the described bug behavior.
class Document(models.Model):
    pass

class Picking(Document):

    def __init_subclass__(cls, **kwargs):
        # Override to ensure the subclass of Document initializes properly regardless of field definitions order.
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'document_ptr'):
            raise AssertionError("document_ptr field is missing!")

try:
    class Picking(Document):
        document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
        origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)
    assert False, "Expected ImproperlyConfigured error due to parent_link misconfiguration"
except ImproperlyConfigured as e:
    # Expected this to happen, print stack trace and exit normally
    print_stacktrace(e)
    exit(0)
except Exception as e:
    print_stacktrace(e)
    assert False, "Unexpected error type"

try:
    class PickingFixed(Document):
        origin = models.OneToOneField(Document, related_name='picking_fixed', on_delete=models.PROTECT)
        document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
        # Expected to work without issues.
except ImproperlyConfigured as e:
    print_stacktrace(e)
    assert False, "The fixed approach should not raise an error"

print("The issue reproduction succeeded without raising the expected error.")

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

if __name__ == "__main__":
    try:
        # Attempt to create models to trigger model validations
        Document.objects.create()
        PickingFixed.objects.create()
    except Exception as e:
        print_stacktrace(e)
```

Please be aware that this script is a simplified representation intended to mimic the described issue's circumstances. The execution and behavior may differ based on your Django project settings, and some adjustments might be needed to perfectly emulate your environment or Django's version specifics.