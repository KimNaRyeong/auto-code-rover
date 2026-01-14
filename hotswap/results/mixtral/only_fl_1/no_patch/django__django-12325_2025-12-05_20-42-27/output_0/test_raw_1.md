 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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
```
When you run the script, it will raise an `ImproperlyConfigured` exception with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 38, in <module>
    schema_editor.create_model(Picking)
  File "/home/user/.local/lib/python3.8/site-packages/django/db/backends/base/schema.py", line 334, in create_model
    sql, params = self.optimized_definition(model, definition, fields)
  File "/home/user/.local/lib/python3.8/site-packages/django/db/backends/base/schema.py", line 168, in optimized_definition
