Here is the reproducer script:

```python
import os
import django
from django.db import models
from django.core.management.commands.makemigrations import CommandError
from unittest.mock import patch, Mock

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

def create_models():
    os.chdir('django_related_name_bug')
    from django.db import models
    class App1(models.Model):
        field = models.ManyToManyField('App2', related_name='+')

    class App2(models.Model):
        pass

if __name__ == '__main__':
    try:
        create_models()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script will change into the directory of your test project, then it will create two models with ManyToManyField. If an error occurs during this process (like the one described in the issue), it will print the stack trace and exit with code 1.