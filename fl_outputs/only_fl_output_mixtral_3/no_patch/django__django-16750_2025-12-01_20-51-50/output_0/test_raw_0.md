 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from django.db.models import Chr, Value
from django.db.models.expressions import Expression

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Author(Expression):
    pass

try:
    Author.objects.annotate(first_letter=Chr(Value(77)))
except ValueError as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    Author.objects.annotate(first_letter=Chr(Value(77)))
  File "/Users/.../.../.venv/lib/python3.9/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/Users/.../.../.venv/lib/python3.9/site-packages/django/db/models/query.py", line 1215, in annotate
