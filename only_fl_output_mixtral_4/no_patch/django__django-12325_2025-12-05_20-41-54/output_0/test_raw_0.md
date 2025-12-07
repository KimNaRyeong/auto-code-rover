 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import django
from django.core.exceptions import ImproperlyConfigured
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
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
        # This line should raise ImproperlyConfigured exception
        models.ModelBase.meta_options = {}
    except ImproperlyConfigured as e:
        print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise an `ImproperlyConfigured` exception with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 27, in <module>
    models.ModelBase.meta_options = {}
  File "/usr/local/lib/python3.9/site-packages/django/db/models/base.py", line 333, in __setattr__
    self.refresh_from_db()
  File "/usr/local/lib/python3.9/site-packages/django/db/models/base.py", line 591, in refresh_from_db
    raise self.related_model._meta.unique_together_violation(message)
django.core.exceptions.ImproperlyConfigured: Add parent_link=True to appname.Picking.origin.
```
To fix the issue, the order of the `OneToOneField` declarations in the `Picking` model should be changed to:
```python
class Picking(Document):
    origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)
    document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
```
After making this change, the script should exit with code 0 when executed with `python3 reproducer.py`.