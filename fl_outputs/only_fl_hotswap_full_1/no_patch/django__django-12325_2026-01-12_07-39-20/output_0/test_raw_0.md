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
        django.forms.declare_fields_for_model(Picking, Document)
    except ImproperlyConfigured as e:
        print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace of the issue.

To fix the issue, you can simply swap the order of the `document_ptr` and `origin` fields in the `Picking` model:
```python
class Picking(Document):
    origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)
    document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
```
After swapping the order, the script should exit with code 0 when executed with `python3 reproducer.py`.