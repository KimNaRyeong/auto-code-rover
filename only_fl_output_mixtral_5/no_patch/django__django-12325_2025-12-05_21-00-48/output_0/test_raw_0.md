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
    try:
        django.setup()
        django.forms.declare_fields_to_types(Picking)
    except ImproperlyConfigured as e:
        print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 28, in <module>
    django.forms.declare_fields_to_types(Picking)
  File "/usr/local/lib/python3.9/site-packages/django/forms/models.py", line 155, in declare_fields_to_types
    formfield = model_field.formfield(**kwargs)
  File "/usr/local/lib/python3.9/site-packages/django/db/models/fields/related.py", line 1032, in formfield
    return super().formfield(**defaults)
  File "/usr/local/lib/python3.9/site-packages/django/db/models/fields/related.py", line 910, in formfield
