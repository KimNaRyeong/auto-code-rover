Here is the reproducer script:

```python
import os
from django.db import models
from django.db.models import Exists
from functools import wraps

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

def assert_raises(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        raise AssertionError("Expected exception not raised")
    except Exception as e:
        print_stacktrace(e)

class Reproducer:
    def __init__(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
        from django.conf import settings
        settings.configure()

    def run(self):
        self._reproduce_issue()

    def _reproduce_issue(self):
        class A(models.Model):
            pass

        class B(models.Model):
            pass

        result = A.objects.annotate(should_be_bool=Exists(B.objects.none())).first().should_be_bool
        if result is None:
            raise AssertionError("Expected boolean value, got None")

if __name__ == '__main__':
    Reproducer().run()
```

This script sets up a Django environment, creates some models and instances of those models, annotates with Exists and checks the result. If the issue is present (i.e., the result is not a boolean), it should raise an AssertionError and print the stack trace.