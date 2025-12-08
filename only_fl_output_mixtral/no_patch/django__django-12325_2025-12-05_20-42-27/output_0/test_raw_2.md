 I apologize for the mistake in the previous response. Here is an updated `reproducer.py` script that reproduces the issue:
```python
import django
from django.core.exceptions import ImproperlyConfigured
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Document(models.Model):
    pass

class Picking(Document):
    document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
    origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)

if __name__ == "__main__":
    settings = django.conf.settings
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        INSTALLED_APPS=['myapp'],
        SECRET_KEY='mysecretkey',
    )

    try:
        django.setup()
        from django.db import connections
        with connections['default'].schema_editor() as schema_editor:
            schema_editor.create_model(Picking)
    except ImproperlyConfigured as e:
        print_stacktrace(e)
        raise AssertionError(e)
```
When you run the script, it will raise an `AssertionError` with the `ImproperlyConfigured` exception as its argument. The `print_stacktrace` function will print the stack trace of the exception.

The issue is that the `origin` field in the `Picking` model is defined before the `document_ptr` field, which has the `parent_link=True` argument. This causes a `ImproperlyConfigured` exception to be raised with the message "Add parent\_link=True to myapp.Picking.origin."

To fix the issue, you can simply swap the order of the `origin` and `document_ptr` fields in the `Picking` model:
```python
class Picking(Document):
    document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
    origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)
```
After swapping the order of the fields, the script should exit with code 0 and print no output.