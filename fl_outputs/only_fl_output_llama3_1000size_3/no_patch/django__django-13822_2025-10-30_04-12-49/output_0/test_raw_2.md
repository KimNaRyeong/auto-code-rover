Here is the reproducer script:

```python
import os
from django.db import models
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

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

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_related_name_bug.settings'
    
    class Model1(models.Model):
        model2 = models.ManyToManyField('Model2', related_name='+')

    class Model2(models.Model):
        pass

    try:
        settings.INSTALLED_APPS
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected error not raised")

if __name__ == "__main__":
    main()
```

This script sets the DJANGO_SETTINGS_MODULE environment variable to 'django_related_name_bug.settings', which does not exist. This should cause an `ImproperlyConfigured` exception when trying to access the settings module, reproducing the issue described in the bug report.